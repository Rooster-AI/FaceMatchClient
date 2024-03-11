#!/bin/bash

# Prompt for the camera.json file path
echo "Please enter the path to the camera.json file:"
read -r CAMERA_JSON_PATH

# Run the Python script with the provided argument
python facial-recognition-client/client.py "$CAMERA_JSON_PATH"