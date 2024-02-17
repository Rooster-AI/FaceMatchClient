"""
    Provides functions for logging to supabase
"""

import json
import os
import requests

os.chdir(os.path.dirname(__file__))
DATABASE_URL = "http://localhost:5000"


class Logger:
    def __init__(self):
        with open("rooster_config.json", "r") as f:
            data = json.load(f)

        self.device_id = data["device_id"]

    def log(self, message, severity="INFO"):
        print(severity + " : " + message)
        requests.post(
            url=DATABASE_URL + "/logging",
            json={
                "severity": severity,
                "message": message,
                "device_id": self.device_id,
            },
            timeout=30,
        )


logger = Logger()


def log(message, severity="INFO"):
    logger.log(message, severity)
