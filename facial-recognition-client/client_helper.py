# pylint: disable=R0913, C0301
"""
This module provides a class `RapidFaceFollow` for capturing video frames from an IP camera,
keeping only the most recent frame, and making it available for further processing. It uses
OpenCV to access the camera feed and manage the frame queue.
"""

import queue
import threading
import os
import cv2
import time

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
            try:
                ret, frame = self.cap.read()
                if not ret:
                    raise Exception("Failed to capture frame")

                if not self.q.empty():
                    try:
                        self.q.get_nowait()  # discard previous (unprocessed) frame
                    except queue.Empty:
                        pass

                self.q.put(frame)

            except Exception as exp:
                print(f"Error capturing frame: {exp}. Attempting the reconnect...")
                self._reconnect()

    def _reconnect(self):
        """Attempt to reconnect to the camera."""
        self.cap.release()
        connection_attempts = 0
        backoff = 1
        while connection_attempts < 10:
            try:
                self.cap = cv2VideoCapture(self.camera_url)
                if self.cap.isOpened():
                    print("Reconnected to camera successfully.")
                    break
            except Exception as exp:
                print(f"Reconnection attempt {connection_attempts+1} failed: {exp}")

            time.sleep(backoff)
            print(f"Waiting {backoff} seconds before next reconnection attempt...")
            backoff *= 2

            connection_attempts += 1

    def read(self, retry_attempts=3, retry_interval=1):
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
