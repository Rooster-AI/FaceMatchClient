#!/bin/bash

# Function to extract variables from camera.json
extract_variables() {
    local json_file="$1"
    local variable_name="$2"
    local value=$(jq -r ".$variable_name" "$json_file")
    echo "$value"
}

# Extract variables from camera.json
camera_json="/home/rooster-admin/Desktop/camera.json"
protocol=$(extract_variables "$camera_json" "camera-connection.protocol")
camera_ip=$(extract_variables "$camera_json" "camera-connection.camera_ip")
camera_user=$(extract_variables "$camera_json" "camera-connection.camera_user")
camera_pass=$(extract_variables "$camera_json" "camera-connection.camera_pass")
camera_port=$(extract_variables "$camera_json" "camera-connection.camera_port")
camera_extra_url=$(extract_variables "$camera_json" "camera-connection.camera_extra_url")
device_id=$(extract_variables "$camera_json" "device_id")

# Construct docker run command with extracted variables as arguments
docker_command="sudo docker run -d --name rooster-client \
    -e PROTOCOL=$protocol \
    -e CAMERA_IP=$camera_ip \
    -e CAMERA_USER=$camera_user \
    -e CAMERA_PASS=$camera_pass \
    -e CAMERA_PORT=$camera_port \
    -e CAMERA_EXTRA_URL=$camera_extra_url \
    -e DEVICE_ID=$device_id \
    rooster-client"

# Run the Docker container
eval "$docker_command"
