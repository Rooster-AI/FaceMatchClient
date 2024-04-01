FROM nvcr.io/nvidia/l4t-tensorflow:r32.7.1-tf2.7-py3 as builder

FROM python:3.9

COPY --from=builder . /builder

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y cron

# Install dependencies individually to optimize caching
RUN pip3 install --no-cache-dir --upgrade pip setuptools scikit-build
RUN pip3 install tensorflow==2.12
RUN pip3 install "git+https://github.com/Rooster-Ai/rooster-deepface.git"
RUN pip3 install Flask==2.2.2
RUN pip3 install numpy==1.26.2
RUN pip3 install opencv-python-headless
RUN pip3 install pandas==2.1.1
RUN pip3 install Pillow==10.1.0

# Copy cron file to the cron.d directory on container
COPY cron /etc/cron.d/cron

# Give execution access
RUN chmod 0644 /etc/cron.d/cron

# Run cron job on cron file
RUN crontab /etc/cron.d/cron

# Create the log file
RUN touch /var/log/cron.log

# Copy your code into the container
COPY facial-recognition-client facial-recognition-client

CMD cron && python facial-recognition-client/client.py
