from Object_detector import Object_detector
import cv2 as cv


if __name__ == '__main__':
    detector = Object_detector()
    datas = []
    for k in range(1, 8):
        f = cv.imread("img ("+str(k)+").jpg")
        f = cv.resize(f, (int(f.shape[1]/4), int(f.shape[0]/4)))
        datas.append(f)
    x,y,w,h = detector.detect_faces([datas[6]])
    cv.imshow("",datas[0])
    cv.waitKey(0)