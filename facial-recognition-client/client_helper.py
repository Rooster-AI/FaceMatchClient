# pylint: disable=R0913, C0301
"""
This module provides a class `RapidFaceFollow` for capturing video frames from an IP camera,
keeping only the most recent frame, and making it available for further processing. It uses
OpenCV to access the camera feed and manage the frame queue.
"""

import queue
import threading
import os
import time
import cv2

os.chdir(os.path.dirname(__file__))


class RapidFaceFollow:
    """
    RapidFaceFollow class
    """

    def __init__(self, protocol, camera_user, camera_pass, camera_ip, camera_port, camera_extra_url):
        camera_url = (
            f'{protocol}://{camera_user}:{camera_pass}@{camera_ip}:{camera_port}{camera_extra_url}'
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
                continue
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass

            self.q.put(frame)

    def read(self, retry_attempts=5, retry_interval=1):
        """
        Retrieve the most recent frame from the camera.
        """
        for attempt in range(retry_attempts):
            try:
                return self.q.get()
            except queue.Empty:
                time.sleep(retry_interval)
            
        raise queue.Empty("No frames available")

    def close(self):
        """
        Close the camera connection and release resources.
        """
        self.cap.release()
