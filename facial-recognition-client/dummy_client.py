
# pylint: disable=W0718,E1101,C0103

"""
A dummy client to test the server
sends 1 group of images to the server
"""

import base64
import json
import sys
import time
import cv2
import requests

SERVER_URL = "http://13.56.83.102:5000/upload-images"

LOCAL_URL = "http://127.0.0.1:5000/upload-images"
# SERVER_URL = LOCAL_URL


CLOCK_TIME = 0.3


def send_images(url, match=True):
    """
    Encode and send a group of images to the server.
    """
    # read in images from dummy images folder
    start_time = time.time()
    images = []
    path = "data/match_dummy_images/frame_"
    num_images = 14
    file_type = '.png'
    if not match:
        path = "data/nonmatch_dummy_images/frame_"
        num_images = 13
        file_type = '.jpg'

    for i in range(0, num_images):
        image = cv2.imread(f"{path}{i}{file_type}")
        images.append(image)

    print("Start sending images")
    encoded_images = []
    for image in images:
        _, buffer = cv2.imencode(".jpg", image)
        jt = base64.b64encode(buffer).decode()
        encoded_images.append(jt)

    data = json.dumps({"images": encoded_images, "device_id": 1})
    try:
        response = requests.post(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        print(response.text)
    except Exception as exp:
        print("Failed to send images to server", exp)
    print("Finished sending images")
    print(f"Time to read in images: {time.time() - start_time}")


if __name__ == "__main__":
    # if "local" was passed in as an argument, use the local server
    url_ = SERVER_URL
    match_ = True
    if "local" in sys.argv:
        print("Using local server")
        url_ = LOCAL_URL

    if "nonmatch" in sys.argv:
        match_ = False

    send_images(url_, match=match_)
