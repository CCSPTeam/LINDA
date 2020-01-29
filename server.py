import base64
import time
import os
import cv2
from flask import Flask, request, render_template
import re
from ImageProcess.ImageProcess import ImageProcess , Calibration
from ArduinoSerial import ArduinoSerial
from PIL import Image
from io import StringIO, BytesIO
import numpy as np

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
calibration= None

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/capture.html', methods=['GET'])
def capture():
    return render_template('capture.html')


def index():
    return render_template('index.html')


@app.route('/apiCapture', methods=['POST'])
def get_image():
    image_b64 = request.values['canvas_data']
    print(image_b64)
    base64_data = re.sub('^data:image/.+;base64,', '', image_b64)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    t = time.time()
    imgPath= "Image/"+str(t) + '.png'
    img.save(imgPath, "PNG")
    analyse_img(imgPath)
    #image_PIL = Image.open(StringIO(image_b64))
    #image_np = np.array(image_PIL)
    #print('Image received: {}'.format(image_np.shape))

    return ''

def analyse_img(imgPath):
    print(calibration)
    imageProcess = ImageProcess(calibration.eq_x0, calibration.eq_x1, calibration.size_face)
    imageProcess.load_img(imgPath)
    if imageProcess.compute():
        arduino.send(-imageProcess.x_delta,imageProcess.y_delta,100)
    print(imageProcess)
    os.remove(imgPath)

if __name__ == "__main__":
    calibration = Calibration()
    calibration.load(['ImageProcess/img/1m.jpg', 'ImageProcess/img/2m.jpg', 'ImageProcess/img/3m.jpg'],
                     [100, 200, 300])
    calibration.compute()
    arduino = ArduinoSerial()
    arduino.connect("COM7")


    app.run()

