from flask import Flask, request, render_template
import re
from PIL import Image
from io import StringIO
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture.html', methods=['GET'])
def capture():
    return render_template('capture.html')

def index():
    return render_template('index.html')

@app.route('/capture.html', methods=['POST'])
def get_image():
    image_b64 = request.values['imageBase64']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64).decode('base64')
    image_PIL = Image.open(StringIO(image_b64))
    image_np = np.array(image_PIL)
    print('Image received: {}'.format(image_np.shape))
    return ''

@app.route('/', methods=['POST'])
def poste():
    print('Pierrot help me')
    return ''

if __name__ == "__main__":
    app.run()

