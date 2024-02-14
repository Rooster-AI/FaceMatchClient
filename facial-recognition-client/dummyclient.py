"""
A dummy client to test the server
sends 1 group of images to the server
"""

import base64
import json
import cv2
import requests
SERVER_URL = "http://127.0.0.1:5000/upload-images"


def send_images():
    """
    Encode and send a group of images to the server.
    """
    # read in images from dummy images folder
    images = []
    for i in range(0, 7):
        image = cv2.imread(f"data/dummy_images/frame_{i}.png")
        images.append(image)



    print("Start sending images")
    encoded_images = []
    for image in images:
        _, buffer = cv2.imencode('.jpg', image)
        jt = base64.b64encode(buffer).decode()
        encoded_images.append(jt)
    data= json.dumps({"images":encoded_images})
    try:
        response = requests.post(SERVER_URL, data=data, headers={'Content-Type':'application/json'})
        print(response.text)
    except Exception as e:
        print("Failed to send images to server", e)
    print("Finished sending images")

if __name__ == "__main__":
    send_images()