# pylint: disable=W0718, C0413
"""
    This is to update the database to the most recent representations
"""

import os
import requests

os.chdir(os.path.dirname(__file__))
from remote_logger import log

SERVER_URL = "http://13.56.83.102:5000"


def update_database():
    """
    Update the database
    """
    log("Updating Database...")
    model = "arcface"
    backend = "mtcnn"
    try:
        response = requests.get(
            SERVER_URL + "/latest_database",
            params={"model": model, "backend": backend},
            timeout=30,
        )
        if response.status_code == 200:
            with open(
                f"./data/database/representations_{model}_{backend}.pkl", "wb"
            ) as f:
                f.write(response.content)

            log(f"Successful database update {model}-{backend}")

        else:
            log("Failed to update database", "WARNING")

    except Exception as e:
        log("Failed to update database" + str(e), "WARNING")


if __name__ == "__main__":
    update_database()
