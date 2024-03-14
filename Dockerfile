FROM nvcr.io/nvidia/l4t-tensorflow:r32.7.1-tf2.7-py3

FROM python:3.9

# Install Git
RUN apt-get update && \
    apt-get install -y git

# Install dependencies individually to optimize caching
RUN pip3 install --no-cache-dir --upgrade pip setuptools scikit-build
RUN pip3 install tensorflow==2.12
RUN pip3 install "git+https://github.com/Rooster-Ai/rooster-deepface.git"
RUN pip3 install Flask==2.2.2
RUN pip3 install numpy==1.26.2
RUN pip3 install opencv-python-headless
RUN pip3 install pandas==2.1.1
RUN pip3 install Pillow==10.1.0

# Copy your code into the container
COPY facial-recognition-client facial-recognition-client

# Set the entry point to the custom entry point script
ENTRYPOINT ["/entrypoint.sh"]
