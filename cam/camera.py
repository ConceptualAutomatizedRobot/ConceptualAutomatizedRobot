import cv2 as cv
import time
import numpy as np

class Camera:
    _cam = None
    _capture = None

    def __init__(self, cam):
        self._cam = cam
        self._capture = cv.VideoCapture(self._cam)

    def __del__(self):
        self._capture.release()

    def capture(self, wait=None):
        if wait is not None:
            time.sleep(wait)
        ret, img = self._capture.read()
        if ret == True:
            return img
        else:
            return None

    def iterate(self, wait=None, max_count=None):
        count = 0
        while max_count is None or count < max_count:
            img = self.capture(wait)
            if img is not None:
                yield ret
            else:
                raise StopIteration

if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) < 2:
        exit(-1)
    cam = Camera(argv[1])
    img = cam.capture()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', img)
    cv.waitKey(10000)
    cv.imshow('frame', gray)
    cv.waitKey(5000)

    cv.destroyAllWindows()

    x = 0
    for i in cam.iterate():
        cv.imshow('frame', i)
        print(x)
        x += 1
        cv.waitKey(5)
        
    cv.destroyAllWindows()

