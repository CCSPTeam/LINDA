from __future__ import print_function
import requests
import json
import cv2

def post_image(img):
    """ post image and return the response """

    response = requests.post(test_url, data=img, headers=headers)
    return response

addr = 'http://localhost:5000'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img_file = 'lena.jpg'
img = open(img_file, 'rb').read()
post_image(img)


# expected output: {u'message': u'image received. size=124x124'}