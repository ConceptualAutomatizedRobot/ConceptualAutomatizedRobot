import cv2 as cv
import numpy as np
from functools import reduce
from camera import Camera
import pyzbar.pyzbar as zbar
import random
from threading import Thread
from multiprocessing import Pool
import sys
sys.path.insert(0,"../system/")
from event import Event

class Classifier:
    def handle(self, img, draw=False):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        thresh, bw = cv.threshold(gray, 100, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        return img, list(self._handle(gray, img, bw, draw))

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

    def _handle(self, gray, img, bw, draw):
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

def is_mark(i, hierarchy, contours):
    curr = i
    depth = 0
    while (hierarchy[curr][2] != -1):
        if cv.isContourConvex(contours[i]):
            return False
        curr = hierarchy[curr][2]
        depth += 1
    return depth >= 5

class ContourClassifier(Classifier):
    def __init__(self):
        pass

    def _handle(self, gray, img, bw, draw):
        edges = cv.Canny(bw, 100, 200)
        cntimg, cnt, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if hierarchy is not None:
            hierarchy = hierarchy[0]
            marks = []
            for i,h in enumerate(cnt):
            #h = [next, previous, child, parent]
                if is_mark(i, hierarchy, cnt):
                    marks.append(i)
            if len(marks) > 0:
                if draw:
                    borders = []
                    for m in marks:
                        epsilon = 0.1*cv.arcLength(cnt[m], True)
                        approx = cv.approxPolyDP(cnt[m], epsilon, True)
                        cv.drawContours(img, [approx], 0, (0,255,0), 3)
                        x,y,w,h = cv.boundingRect(approx)
                        borders.append(((x,y), (w,h)))
                    x = min([x for (x,y), (w,h) in borders])
                    y = min([y for (x,y), (w,h) in borders])
                    w = max([x+w for (x,y), (w,h) in borders]) - x
                    h = max([y+h for (x,y), (w,h) in borders]) - y
                    l = max(w,h)
                    cv.rectangle(img, (x,y), (x+l,y+l), (255,0,0), 2)

                    roi = bw[y:y+h+1,x:x+w+1]
                    decoded = zbar.decode(roi, symbols=[zbar.ZBarSymbol.QRCODE])

                    yield (x,y,w,h), (int(x+w/2), int(y+h/2)), decoded

class SlidingClassifier(Classifier):
    def _handle(self, gray, img, bw, draw):
        decoded = zbar.decode(bw, symbols=[zbar.ZBarSymbol.QRCODE])
        for code in decoded:
            x,y = 0,0
            h,w = bw.shape
            H,W = bw.shape
            found = True
            while found:
                found = False
                margin_x = W-w
                margin_y = H-h
                cur_x, cur_y = x,y
                while cur_x + w <= W:
                    while cur_y + h <= H:
                        roi = bw[cur_y:cur_y+h+1, cur_x:cur_x+w+1]
                        test = zbar.decode(roi, symbols=[zbar.ZBarSymbol.QRCODE])
                        if code in test:
                            x = max(x,cur_x)
                            y = max(y,cur_y)
                            W = min(W,cur_x+w)
                            H = min(H,cur_y+h)
                            found = True
                        cur_x += 2
                        cur_y += 2
                w -= 2
                h -= 2
            yield (x,y,w,h), (int(x+w/2), int(y+h/2)), code

class SplittingClassifier(Classifier):
    def _handle(self, gray, img, bw, draw):
        decoded = zbar.decode(bw, symbols=[zbar.ZBarSymbol.QRCODE])
        h,w = bw.shape
        if draw:
                cv.rectangle(img, (0,0), (int(w/2)-2,h), (255,0,0), 2)
                cv.rectangle(img, (int(w/2)+2, 0), (w,h), (255,128,0), 2)
                cv.rectangle(img, (4,4), (w-5, int(h/2)-2), (0,255,0), 2)
                cv.rectangle(img, (4,int(h/2)+2), (w-5,h-5), (0,0,255), 2)
        if len(decoded) > 0:
            left = bw[:,:int(w/2)]
            right = bw[:,int(w/2):]
            top = bw[:int(h/2),:]
            bottom = bw[int(h/2):,:]
            ltest = zbar.decode(left, symbols=[zbar.ZBarSymbol.QRCODE])
            rtest = zbar.decode(right, symbols=[zbar.ZBarSymbol.QRCODE])
            ttest = zbar.decode(top, symbols=[zbar.ZBarSymbol.QRCODE])
            btest = zbar.decode(bottom, symbols=[zbar.ZBarSymbol.QRCODE])
            for code in decoded:
                if code in ltest and not code in rtest:
                    lr = -1
                elif code not in ltest and code in rtest:
                    lr = 1
                else:
                    lr = 0
                if code in ttest and not code in btest:
                    tb = 1
                elif code not in ttest and code in btest:
                    tb = -1
                else:
                    tb = 0
                yield lr,tb,code
                #if code in ltest and code not in rtest:
                    #yield (0,0,int(w/2),h), (int(w/4),int(h/2)), code
                #elif code not in ltest and code in rtest:
                    #yield (int(w/2), 0, int(w/2),h), (int(3*w/4), int(h/2)), code
                #else:
                    #yield (0,0,w,h), (int(w/2), int(h/2)), code

class NoClassifier(Classifier):
    def _handle(self, gray, img, bw, draw):
        w,h = bw.shape
        if draw:
            cv.rectangle(img, (0,0), (h,w), (255,0,0), 2)
            decoded = zbar.decode(bw, symbols=[zbar.ZBarSymbol.QRCODE])
        yield (0,0,h,w), (w/2,h/2), decoded

class OffloadedClassifier(Thread):
    def __init__(self, S, classifier, feed, target, draw=False, resolution=1.):
        super(OffloadedClassifier, self).__init__()
        self._S = S
        self._class = classifier
        self._feed = feed
        self._target = target
        self._draw = draw
        self._continue = True
        self._resolution = resolution

    def run(self):
        with Pool(processes=2) as pool:
            for img, l in pool.imap(self._class.handle, self._feed.iterate()):
                if self._draw:
                    shape = tuple([self._resolution * x for x in img.shape])
                    cv.imshow('frame', cv.resize(img, shape))
                    cv.waitKey(1)
                for lr,tb,code in l:
                    s = code[0].decode("utf-8")
                    if s == self._target:
                        self._S.notify(Event(self._S.E_XPOS, lr))
                        self._S.notify(Event(self._S.E_YPOS, tb))
                if not self._continue:
                    return
    def stop(self):
        self._continue = False


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
    classifiers.add_argument('--none', action='store_const', const='none', dest='classifier')
    classifiers.add_argument('--slide', action='store_const', const='slide', dest='classifier')
    classifiers.add_argument('--split', action='store_const', const='split', dest='classifier')

    parser.add_argument('--resolution', type=float, default=1.)
    parser.add_argument('--fps', type=int)
    parser.add_argument('--offload', action='store_true')

    args = parser.parse_args()

    cam = Camera(args.video, fps=args.fps)
    if args.classifier == 'body':
        cl = BodyClassifier()
    elif args.classifier == 'homo':
        ref = cv.imread('ref2.png', cv.IMREAD_UNCHANGED)
        cl = HomoClassifier(ref)
        cv.imshow('ref', ref)
        cv.waitKey(1000)
        cv.destroyAllWindows()
    elif args.classifier == 'contour':
        cl = ContourClassifier()
    elif args.classifier == 'none':
        cl = NoClassifier()
    elif args.classifier == 'slide':
        cl = SlidingClassifier()
    elif args.classifier == 'split':
        cl = SplittingClassifier()
    else:
        exit(-2)

    if not args.offload:
        for img,y in cl.map(cam.iterate(), args.show):
            if args.show:
                dsize = None
                dst = None
                resized = cv.resize(img, dst, dsize, args.resolution, args.resolution)
                cv.imshow('frame', resized)
            print(y)
            cv.waitKey(1)
    else:
        off = OffloadedClassifier(None, cl, cam, "abc", args.show)
        off.start()
        off.join()
