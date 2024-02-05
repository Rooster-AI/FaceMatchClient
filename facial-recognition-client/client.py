"""
This module contains a client script for capturing frames from a video feed and performing face recognition.
The client captures frames and switches to face recognition mode when it detects faces in the frames.
It uses the DeepFace library to perform face recognition and sends matched faces to a server.
"""
from concurrent.futures import ThreadPoolExecutor
import json
import cv2
from client_helper import RapidFaceFollow
from deepface import DeepFace
import time
import os
import requests
import base64

os.chdir(os.path.dirname(__file__))

CLOCK_TIME = 0.3
FRAME_GROUP_SIZE = 12
DB = "data/database"
SERVER_URL = "http://127.0.0.1:5000/upload-images"

def check_face(frame, send_signals, num):
    """
    Perform face recognition on a given frame and update the send_signals list based on the result.
    """
    try:
        result = DeepFace.find(
            img_path=frame,
            db_path=DB,
            model_name="ArcFace",
            distance_metric="cosine",
            enforce_detection=True,
            detector_backend="mtcnn",
            silent=True
        )
    except Exception as e:
        print("No Match, signaling", e)
        send_signals.append(f"NO_MATCH")
    else:
        if len(result) > 0 and len(result[0]['identity'].to_list()) > 0:
            print("Matched a face, preliminary match:", result[0]['identity'].to_list()[0])
            send_signals.append(f"MATCHED")
        else:
            print("No Faces Match, signaling")
            send_signals.append(f"NO_MATCH")
    finally:
        print("Finished Matching")
        send_signals.append(f"FINISHED_{num}")

    return

def send_images(images):
    """
    Encode and send a group of images to the server.
    """
    print("Start sending images")
    encoded_images = []
    for image in images:
        _, buffer = cv2.imencode('.jpg', image)
        jt = base64.b64encode(buffer).decode()
        encoded_images.append(jt)
    data= json.dumps({"images":encoded_images})
    print('encoding done')
    response = requests.post(SERVER_URL, data=data, headers={'Content-Type':'application/json'})
    if response.status_code == 200:
        result = response.json()
        print('status of post',result['status'])
    else:
        print('Error in post:', response.status_code)

    return


def client():
    # TODO: initialize arcface and mtcnn model
    feed = RapidFaceFollow()
    face_mode = False
    frame_group = []
    send_signals = [] # FINISHED_2 | FINSIHED_5 | NO_MATCH | MATCHED
    with ThreadPoolExecutor(max_workers=2) as executor:
        print("Starting: Caputuring Frames")
        while True:
            start_time = time.time()
            try:
                frame = feed.read()
            except Exception as e:
                print(e)

            if face_mode:
                group_size = len(frame_group)
                if group_size <= FRAME_GROUP_SIZE:
                    frame_group.append(frame)
                if group_size == 2:
                    print("Starting to check 2nd frame")
                    executor.submit(check_face, frame, send_signals, 2)
                elif group_size == 5:
                    print("Starting to check 5th frame")
                    executor.submit(check_face, frame, send_signals, 5)
                elif group_size >= FRAME_GROUP_SIZE:
                    if "FINISHED_2" in send_signals and "FINISHED_5" in send_signals:
                        if "MATCHED" in send_signals:
                            print("Matched, sending to server")
                            # Send frames to server
                            executor.submit(send_images, frame_group)
                            frame_group = []
                            send_signals = []
                            face_mode = False
                        elif "NO_MATCH" in send_signals:
                            print("Not matched, restarting")
                            frame_group = []
                            send_signals = []
                            face_mode = False
                    else:
                        print("WAITING TO FINISH MATCHING")

            else:
                try:
                    faces = DeepFace.extract_faces(frame, detector_backend="opencv")
                    faces = [f for f in faces if f["confidence"] > 7]
                except:
                    pass
                else:
                    if len(faces):
                        print("Starting Face Mode")
                        face_mode = True
                        frame_group.append(frame)

            left_time = CLOCK_TIME - (time.time() - start_time)
            if left_time > 0:
                # print("extra time", left_time)
                time.sleep(left_time)


if __name__ == "__main__":
    client()
