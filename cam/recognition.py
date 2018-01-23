import cv2 as cv
import numpy as np
from camera import Camera

class Classifier:
    def handle(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        result = []
        for lims in self._handle(gray, img):
            result.append(lims)

        return img, result

    def map(self, it):
        for img in it:
            yield self.handle(img)

class BodyClassifier(Classifier):
    _classifier = None
    def __init__(self):
        #self._classifier = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_lowerbody.xml')
        self._classifier = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def _handle(self, gray, img):
        detected = self._classifier.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in detected:
            cv.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
            yield (x,y,w,h), (x+w/2, y+h/2)

class HomoClassifier(Classifier):
    _ref = None
    def __init__(self, ref):
        self._ref = cv.cvtColor(ref, cv.COLOR_BGR2GRAY)
        self._sift = cv.xfeatures2d.SIFT_create()
        self._kp, self._des = self._sift.detectAndCompute(self._ref, None)
        FLANN_INDEX_KDTREE = 1
        self._index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        self._search_params = dict(checks = 50)
        self._flann = cv.FlannBasedMatcher(self._index_params, self._search_params)

    def _handle(self, gray, img):
        kp, des = self._sift.detectAndCompute(gray, None)
        if len(kp) > 2 and len(self._kp) > 2:
            matches = self._flann.knnMatch(self._des, des, k=2)

            good = []
            for m,n in matches:
                if m.distance < 0.7*n.distance:
                    good.append(m)
            if len(good) > 10:
                src_pts = np.float32([ self._kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([ kp[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                
                M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
                matchesMask = mask.ravel().tolist()
                if M is not None:
                    h,w = self._ref.shape
                    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                    dst = cv.perspectiveTransform(pts,M)
                    
                    dst = np.array(list(map(lambda x: x[0], dst)))
                    centroid = (
                        int(sum(map(lambda x: x[0], dst))/len(dst)),
                        int(sum(map(lambda x: x[1], dst))/len(dst)))
                    
                    cv.polylines(img,[np.int32(dst)],True,(0,255,0),3, cv.LINE_AA)
                    cv.circle(img, centroid, 20, (0,255,0))

                    yield dst,centroid

if __name__ == '__main__':
    from sys import argv, exit
    import time

    if len(argv) < 3:
        exit(-1)


    cam = Camera(argv[1], fps=0.5)
    if argv[2] == 'haar':
        cl = BodyClassifier()
    elif argv[2] == 'homo':
        ref = np.load('ref.npy')
        cl = HomoClassifier(ref)
        cv.imshow('ref', ref)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        exit(-2)

    for x,y in cl.map(cam.iterate()):
        cv.imshow('frame', x)
        cv.waitKey(1)
