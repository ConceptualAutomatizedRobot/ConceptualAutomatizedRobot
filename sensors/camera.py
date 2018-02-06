import cv2 as cv
import time
import numpy as np

class Camera:
    _cam = None
    _capture = None

    def __init__(self, cam, fps=None, resolution=None):
        self._cam = cam
        self._capture = cv.VideoCapture(self._cam)
        if fps is not None:
            self._capture.set(cv.CAP_PROP_FPS, fps)
        if resolution is not None:
            w = self._capture.get(cv.CAP_PROP_FRAME_WIDTH)
            h = self._capture.get(cv.CAP_PROP_FRAME_HEIGHT)
            self._capture.set(cv.CAP_PROP_FRAME_WIDTH, w*resolution)
            self._capture.set(cv.CAP_PROP_FRAME_HEIGHT, h*resolution)


    def __del__(self):
        self._capture.release()

    def capture(self):
        ret, img = self._capture.read()
        if ret == True:
            return img
        else:
            return None

    def iterate(self, max_count=None):
        count = 0
        while max_count is None or count < max_count:
            img = self.capture()
            if img is not None:
                yield img
                count += 1
            else:
                raise StopIteration

if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) < 2:
        exit(-1)
    cam = Camera(argv[1])

    for img in cam.iterate():
        cv.imshow('frame', img)
        r = cv.waitKey(50)
        if r == 113: # q
            np.save('ref', img)
            exit(0)
        
    cv.destroyAllWindows()

