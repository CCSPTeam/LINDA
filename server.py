import base64
import time

import cv2
from flask import Flask, request, render_template
import re
from PIL import Image
from io import StringIO, BytesIO
import numpy as np
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/capture.html', methods=['GET'])
def capture():
    return render_template('capture.html')


def index():
    return render_template('index.html')


@app.route('/apiCapture', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_image():
    image_b64 = request.values['canvas_data']
    print(image_b64)
    base64_data = re.sub('^data:image/.+;base64,', '', image_b64)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    t = time.time()
    img.save("" + str(t) + '.png', "PNG")

    image_PIL = Image.open(StringIO(image_b64))
    image_np = np.array(image_PIL)
    print('Image received: {}'.format(image_np.shape))
    return ''


if __name__ == "__main__":
    app.run()

