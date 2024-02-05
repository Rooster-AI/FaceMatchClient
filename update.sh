#!/bin/bash

# Run 'git pull' in the current directory
git pull

# Check if 'git pull' was successful
if [ $? -eq 0 ]; then
    echo "Git pull successful."

    # URL of the file you want to download
    file_url="https://userooster.com/download_database/db.pkl"

    # Destination path where you want to save the downloaded file
    destination_path="./database.pkl"

    # Download the file using 'curl'
    curl -o "$destination_path" "$file_url"

    # Check if 'curl' was successful
    if [ $? -eq 0 ]; then
        echo "File downloaded successfully."
    else
        echo "Error: Failed to download the file."
    fi
else
    echo "Error: Git pull failed. Please check your Git repository."
fi
