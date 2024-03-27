#!/bin/bash

# Extract variables from camera.json
camera_json="./facial-recognition-client/rooster_config.json"
protocol=$(jq -r '.["camera-connection"].protocol' "$camera_json")
camera_ip=$(jq -r '.["camera-connection"].camera_ip' "$camera_json")
camera_user=$(jq -r '.["camera-connection"].camera_user' "$camera_json")
camera_pass=$(jq -r '.["camera-connection"].camera_pass' "$camera_json")
camera_port=$(jq -r '.["camera-connection"].camera_port' "$camera_json")
camera_extra_url=$(jq -r '.["camera-connection"].camera_extra_url' "$camera_json")
device_id=$(jq -r '.device_id' "$camera_json")

# Check if the container already exists and remove it if it does
existing_container=$(sudo docker ps -aq -f name=^/rooster-client$)
if [ ! -z "$existing_container" ]; then
    echo "Container named '/rooster-client' already exists, removing..."
    sudo docker rm -f "$existing_container"
fi

# Construct docker run command with extracted variables as arguments
docker_command="sudo docker run -d --name rooster-client \
    -e PROTOCOL=\"$protocol\" \
    -e CAMERA_IP=\"$camera_ip\" \
    -e CAMERA_USER=\"$camera_user\" \
    -e CAMERA_PASS=\"$camera_pass\" \
    -e CAMERA_PORT=\"$camera_port\" \
    -e CAMERA_EXTRA_URL=\"$camera_extra_url\" \
    -e DEVICE_ID=\"$device_id\" \
    --restart always \
    roosteradmin/rooster-client"

# Run the Docker container
eval "$docker_command"