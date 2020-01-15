import cv2
import numpy as np

class Object_detector:
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.coef_width = 1
        self.coef_height = 1
        self.width_pierre = 10 # Unit : cm
        self.height_pierre = 20 # Unit : cm

    def detect_faces(self, images):
        x, y, w, h = [], [], [], []
        for img in images:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.5,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in faces:
                x.append(x)
                y.append(y)
                w.append(w)
                h.append(h)
        x = np.mean(x)
        y = np.mean(y)
        w = np.mean(w)
        h = np.mean(h)

        return x,y,w,h

    def computeXYZ(self, x,y,w,h):
        z = 0.5 * (self.coef_width/w + self.coef_height/h)
        x_real = x/w*self.width_pierre
        y_real = y/h*self.height_pierre

        return x_real, y_real, z
