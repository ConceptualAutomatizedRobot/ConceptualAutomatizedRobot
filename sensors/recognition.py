import cv2 as cv
import numpy as np
from functools import reduce
from camera import Camera
#import pyzbar.pyzbar as zbar

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

def children(i, hierarchy):
    curr = hierarchy[i][2]
    while curr != -1:
        yield curr
        curr = hierarchy[curr][0]

def is_mark(i, hierarchy):
    curr = i
    depth = 0
    while (hierarchy[curr][2] != -1):
        curr = hierarchy[curr][2]
        depth += 1
    if (hierarchy[curr][2] != -1):
        depth += 1
    return depth == 5

class ContourClassifier(Classifier):
    def __init__(self):
        pass

    def _handle(self, gray, img, draw):
        edges = cv.Canny(gray, 100, 200)
        cntimg, cnt, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if hierarchy is not None:
            hierarchy = hierarchy[0]
            #print(cnt)
            marks = []
            for i,h in enumerate(cnt):
            #h = [next, previous, child, parent]
                for c in children(i, hierarchy):
                      if is_mark(c, hierarchy):
                        marks.append(i)
            if len(marks) > 0:
                print(marks)
            if draw:
                for m in marks:
                    cv.drawContours(img, cnt, m, (0,255,0), 3)
        
        yield None

if __name__ == '__main__':
    from sys import argv, exit
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--video', required=True)

    show = parser.add_mutually_exclusive_group()
    show.add_argument('--noshow', action='store_false', dest='show')
    show.add_argument('--show', action='store_true', dest='show', default=True)

    classifiers = parser.add_mutually_exclusive_group(required=True)
    classifiers.add_argument('--body', action='store_const', const='body', dest='classifier')
    classifiers.add_argument('--homo', action='store_const', const='homo', dest='classifier')
    classifiers.add_argument('--contour', action='store_const', const='contour', dest='classifier')

    parser.add_argument('--resolution', type=float)

    args = parser.parse_args()

    cam = Camera(args.video, resolution=args.resolution, fps=10)
    if args.classifier == 'body':
        cl = BodyClassifier()
    elif args.classifier == 'homo':
        ref = cv.imread('ref.png', cv.IMREAD_UNCHANGED)
        cl = HomoClassifier(ref)
        cv.imshow('ref', ref)
        cv.waitKey(1000)
        cv.destroyAllWindows()
    elif args.classifier == 'contour':
        cl = ContourClassifier()
    else:
        exit(-2)

    for x,y in cl.map(cam.iterate(), args.show):
        if args.show:
            cv.imshow('frame', x)
        print(y)
        cv.waitKey(1)
