# Facial Recognition Client

## Introduction

This is the Rooster client-side code for facial recogntion and verification. This code will be deployed onto local devices (ex. Raspberry-pi). This client will be focused on finding faces in camera frames and doing an initial match before passing the frames to the server. 

## Prerequisites

Before running this server, ensure you have the following dependencies installed:

- Python
- Required Python packages (listed in `requirements.txt`)

## Getting Started

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/Rooster-AI/FaceMatchClient.git
2. Run bash setup.sh
3. Set Regular git pull and database download:
   a. crontab -e
   b. add this line to the file: 0 3 * * * /path/to/your/bash/update.sh
4. Make sure when making changes you branch from **staging**
5. Make a pull request for your changes and have another dev review it


## Config
rooster_config.json contains connection info for the camera, and also the device_id which should correspond to a client in the database
