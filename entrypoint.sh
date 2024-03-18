#!/bin/bash

# Extract variables from camera.json
camera_json="/home/rooster-admin/Desktop/rooster_config.json"
protocol=$(jq -r '.["camera-connection"].protocol' "$camera_json")
camera_ip=$(jq -r '.["camera-connection"].camera_ip' "$camera_json")
camera_user=$(jq -r '.["camera-connection"].camera_user' "$camera_json")
camera_pass=$(jq -r '.["camera-connection"].camera_pass' "$camera_json")
camera_port=$(jq -r '.["camera-connection"].camera_port' "$camera_json")
camera_extra_url=$(jq -r '.["camera-connection"].camera_extra_url' "$camera_json")
device_id=$(jq -r '.device_id' "$camera_json")

# Construct docker run command with extracted variables as arguments
docker_command="sudo docker run  --name rooster-client \
    -e PROTOCOL=\"$protocol\" \
    -e CAMERA_IP=\"$camera_ip\" \
    -e CAMERA_USER=\"$camera_user\" \
    -e CAMERA_PASS=\"$camera_pass\" \
    -e CAMERA_PORT=\"$camera_port\" \
    -e CAMERA_EXTRA_URL=\"$camera_extra_url\" \
    -e DEVICE_ID=\"$device_id\" \
    rooster-client"

# Run the Docker container
eval "$docker_command"

