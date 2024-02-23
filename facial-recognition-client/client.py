"""
Client script for capturing frames, performing face recognition, and sending results to a server
Captures frames, switches to face recognition when faces are detected, and uses the DeepFace library
"""

from concurrent.futures import ThreadPoolExecutor
import json
import time
import os
import base64
import queue
import cv2
from deepface import DeepFace
import requests

os.chdir(os.path.dirname(__file__))
from client_helper import RapidFaceFollow
from remote_logger import log


# import logging
# from logging.handlers import RotatingFileHandler

# # Make sure the working directory is from this file


# # Create a logger
# logger = logging.getLogger('rooster_client')
# logger.setLevel(logging.INFO)

# # Create a handler that writes log messages to a file, with a maximum
# # log file size of 5MB and keeping backup logs (e.g., 3 old log files).
# handler = RotatingFileHandler('rooster_client.log', maxBytes=5*1024*1024, backupCount=10)
# formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
# handler.setFormatter(formatter)

# # Add the handler to the logger
# logger.addHandler(handler)

# # Now you can log messages
# #logger.info('Start Client')


# Constants
CLOCK_TIME = 0.4
FRAME_GROUP_SIZE = 12
MODEL = "ArcFace"
BACKEND = "mtcnn"
DB = "data/database"
SERVER_URL = "http://3.101.40.95:5000/upload-images"
LOCAL_URL = "http://127.0.0.1:5000/upload-images"
# SERVER_URL = LOCAL_URL


def initialize_video_feed():
    """
    Initializes the video feed for capturing frames.
    """
    feed = RapidFaceFollow()
    # logger.info("Feed Initialized")
    return feed


def check_face(frame, send_signals, num):
    """
    Perform face recognition on a given frame and update the send_signals list based on the result.
    """
    try:
        result = DeepFace.find(
            img_path=frame,
            db_path=DB,
            model_name=MODEL,
            distance_metric="cosine",
            enforce_detection=True,
            detector_backend=BACKEND,
            silent=True,
        )
    except ValueError:
        # logger.info("No Match, signaling")
        send_signals.append("NO_MATCH")
    else:
        if len(result) > 0 and len(result[0]["identity"].to_list()) > 0:
            # logger.info(
            #     "Matched a face, preliminary match:" + str(result[0]["identity"].to_list()[0])
            # )
            send_signals.append("MATCHED")
        else:
            # logger.info("No Faces Match, signaling")
            send_signals.append("NO_MATCH")
    finally:
        # logger.info("Finished Matching")
        send_signals.append(f"FINISHED_{num}")


def send_images(images):
    """
    Encode and send a group of images to the server.
    """
    # logger.info("Start sending images to server")
    encoded_images = []
    for image in images:
        _, buffer = cv2.imencode(".jpg", image)
        encoded_image = base64.b64encode(buffer).decode()
        encoded_images.append(encoded_image)
    data = json.dumps({"images": encoded_images})
    print("sending to server")
    response = requests.post(
        SERVER_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        timeout=None,
    )
    if response.status_code == 200:
        result = response.json()
        print(result)
        # logger.info("Status from server" + str(result["status"]))
    else:
        pass
        # logger.warning("Error in post to server:" +  str(response.status_code))


def process_frame_for_face_recognition(
    feed, face_mode, frame_group, send_signals, executor
):
    """
    Processes frames from the video feed for face recognition.
    """
    try:
        frame = feed.read()
    except queue.Empty:
        return face_mode, frame_group, send_signals

    if face_mode:
        group_size = len(frame_group)
        if group_size < FRAME_GROUP_SIZE:
            frame_group.append(frame)
        if group_size == 2:
            # logger.debug("Starting to check 2nd frame")
            executor.submit(check_face, frame, send_signals, 2)
        elif group_size == 5:
            # logger.debug("Starting to check 5th frame")
            executor.submit(check_face, frame, send_signals, 5)
        elif group_size >= FRAME_GROUP_SIZE:
            face_mode = manage_communication_with_server(
                frame_group, send_signals, executor
            )
    else:
        try:
            faces = DeepFace.extract_faces(frame, detector_backend="opencv")
            if len(faces) > 0:
                # logger.debug("Starting Face Mode")
                print("Face found")
                face_mode = True
                frame_group.append(frame)
        except ValueError:
            pass

    return face_mode, frame_group, send_signals


def manage_communication_with_server(frame_group, send_signals, executor):
    """
    Manages the communication with the server to send frames after successful face recognition.
    """
    if "FINISHED_2" in send_signals and "FINISHED_5" in send_signals:
        if "MATCHED" in send_signals:
            print("Matched, sending to server")
            executor.submit(send_images, frame_group[:])
            frame_group.clear()
            send_signals.clear()
            return True
        if "NO_MATCH" in send_signals:
            print("Not matched, restarting")
            frame_group.clear()
            send_signals.clear()
            return False
    # print("WAITING TO FINISH MATCHING")
    return True


def client():
    """
    Main function for the client script.
    """
    log("Initialized Client", "IMPORTANT")
    feed = initialize_video_feed()
    face_mode = False
    frame_group = []
    send_signals = []
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            # logger.info("Starting: Caputuring Frames")
            while True:
                start_time = time.time()
                face_mode, frame_group, send_signals = (
                    process_frame_for_face_recognition(
                        feed, face_mode, frame_group, send_signals, executor
                    )
                )

                left_time = CLOCK_TIME - (time.time() - start_time)
                if left_time > 0:
                    time.sleep(left_time)
    except (KeyboardInterrupt, Exception) as e:
        log("CLIENT DOWN" + str(e), "WARNING")


if __name__ == "__main__":
    client()
