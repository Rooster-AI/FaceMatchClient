"""
This module provides a class `RapidFaceFollow` for capturing video frames from an IP camera,
keeping only the most recent frame, and making it available for further processing. It uses
OpenCV to access the camera feed and manage the frame queue.
"""

import queue
import threading
import cv2
import json
import os

os.chdir(os.path.dirname(__file__))


class RapidFaceFollow:
    """
    RapidFaceFollow class
    """

    def __init__(self):
        # Load camera config from json
        with open("rooster_config.json", "r") as f:
            data = json.load(f)["camera-connection"]

        camera_url = (
            f'{data["protocol"]}://{data["camera_user"]}:{data["camera_pass"]}'
            f'@{data["camera_ip"]}:{data["camera_port"]}{data["camera_extra_url"]}'
        )
        self.cap = cv2.VideoCapture(camera_url)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        """
        Retrieve the most recent frame from the camera.
        """
        return self.q.get()

    def close(self):
        """
        Close the camera connection and release resources.
        """
        self.cap.release()
