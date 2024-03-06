# pylint: disable=W0718, R0903
"""
    Provides functions for logging to supabase
"""

import json
import os
import requests

os.chdir(os.path.dirname(__file__))
DATABASE_URL = "http://13.56.83.102:5000"


class Logger:
    """
    Does Remote Logging for the client device
    """
    def __init__(self):
        with open("rooster_config.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.device_id = data["device_id"]

    def log(self, message, severity="INFO"):
        """
        Sends log to database
        """
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
    """
    Sends log to log file
    """
    logger.log(message, severity)
