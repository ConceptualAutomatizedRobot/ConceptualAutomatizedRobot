import cv2 as cv
import numpy as np
from functools import reduce
from camera import Camera
import pyzbar.pyzbar as zbar

class Classifier:
    def handle(self, img, draw=False):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        return img, list(self._handle(gray, img, draw))

    def map(self, it, draw=False):
        for img in it:
            yield self.handle(img, draw)

class BodyClassifier(Classifier):
    _classifier = None
    def __init__(self):
        #self._classifier = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_lowerbody.xml')
        self._classifier = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def _handle(self, gray, img, draw):
        for (x,y,w,h) in self._classifier.detectMultiScale(gray, 1.3, 5):
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

    def _handle(self, gray, img, draw):
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
                    centroid = tuple(int(x/len(dst)) for x in reduce(lambda x,y: (x[0]+y[0], x[1]+y[1]), dst, (0,0)))
                    min_x = min(map(lambda x: int(x[0]), dst))
                    max_x = max(map(lambda x: int(x[0]), dst))
                    min_y = min(map(lambda x: int(x[1]), dst))
                    max_y = max(map(lambda x: int(x[1]), dst))
                    
                    max_x = min(max_x, gray.shape[1])
                    max_y = min(max_y, gray.shape[0])
                    min_x = max(min_x, 0)
                    min_y = max(min_y, 0)
                    #roi = gray[min_y:max_y+1,min_x:max_x+1]
                    #decoded = zbar.decode(roi, symbols=[zbar.ZBarSymbol.QRCODE])
                    decoded = None
                    if draw:
	                    cv.polylines(img,[np.int32(dst)],True,(0,255,0),3, cv.LINE_AA)
	                    cv.circle(img, centroid, 20, (0,255,0))


                    yield dst,centroid,decoded

class ContourClassifier
	def __init__(self):
		pass

	def _handle(self, gray, img, draw):
		pass

if __name__ == '__main__':
    from sys import argv, exit
    import time

    if len(argv) < 3:
        exit(-1)


    cam = Camera(argv[1], fps=0.5)
    if argv[2] == 'haar':
        cl = BodyClassifier()
    elif argv[2] == 'homo':
        ref = cv.imread('ref.png', cv.IMREAD_UNCHANGED)
        cl = HomoClassifier(ref)
        cv.imshow('ref', ref)
        cv.waitKey(1000)
        cv.destroyAllWindows()
    else:
        exit(-2)

    for x,y in cl.map(cam.iterate(), True):
        cv.imshow('frame', x)
        print(y)
        cv.waitKey(1)
