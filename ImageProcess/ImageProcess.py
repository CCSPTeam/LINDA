import cv2
import numpy as np


class Calibration:
    def __init__(self, size_face=20):
        self.tab_img = []
        self.data = []
        self.size_face = size_face
        self.eq_x0, self.eq_x1, self.tab_measure = None, None, None

    def load(self, tab_path_img, tab_measure):
        self.tab_measure = tab_measure
        for path_img in tab_path_img:
            self.tab_img.append(cv2.imread(path_img))

    def compute(self):
        for img in self.tab_img:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.data.append(detect_face(gray))
        eq = np.polyfit(np.array([self.data[0][2], self.data[1][2], self.data[2][2]]), np.array(self.tab_measure), 1)
        self.eq_x1 = eq[0]
        self.eq_x0 = eq[1]

    def __repr__(self):
        return "Calibration \n" \
               + "eq        :" + str(self.eq_x1) + " * x + " + str(self.eq_x0) + "\n" \
               + "size_face : " + str(self.size_face)


class ImageProcess:
    def __init__(self, calibration):
        self.equation_x0 = calibration.eq_x0
        self.equation_x1 = calibration.eq_x1
        self.size_face = calibration.size_face
        self.h, self.w, self.y, self.x = 0, 0, 0, 0
        self.img, self.img_gray = None, None
        self.distance = 0
        self.x_delta = 0
        self.y_delta = 0

    def load_img(self, path_img):
        self.img = cv2.imread(path_img)
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def show(self):
        cv2.imshow('img', self.img)
        cv2.waitKey()

    def compute(self):
        [self.x, self.y, self.w, self.h] = detect_face(self.img_gray)
        self.distance = (self.equation_x0 + self.equation_x1 * self.w)
        self.x_delta = (self.x - int(self.img.shape[1] / 2)) / self.w * self.size_face
        self.y_delta = (self.y - int(self.img.shape[0] / 2)) / self.w * self.size_face

    def __repr__(self):
        return "ImageProcess" + "\n" \
               + "distance : " + str(self.distance) + "\n" \
               + "x_delta  : " + str(self.x_delta) + "\n" \
               + "y_delta  : " + str(self.y_delta)


def detect_face(img_gray):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)
    if len(faces) != 1:
        return False
    for (x, y, w, h) in faces:
        t = [x, y, w, h]
        cv2.rectangle(img_gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return t


if __name__ == '__main__':
    # Calibration
    calibration = Calibration()
    calibration.load(['img(1m).jpg', 'img(2m).jpg', 'img(3m).jpg'], [100, 200, 300])
    calibration.compute()
    print(calibration)

    # Image Process
    imageProcess = ImageProcess(calibration)
    imageProcess.load_img('test (3).jpg')
    imageProcess.compute()
    print(imageProcess)

    # Information for next bloc :
    # imageProcess.distance
    # imageProcess.x_delta
    # imageProcess.y_delta
