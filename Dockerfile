FROM nvcr.io/nvidia/l4t-base:r36.2.0 as builder

FROM python:3.9
COPY --from=builder . /builder
# Copy requirements file and install dependencies

# Install dependencies individually to optimize caching
RUN pip install "git+https://github.com/Rooster-Ai/rooster-deepface.git"
RUN pip install Flask==2.2.2
RUN pip install numpy==1.26.2
RUN pip install opencv-python-headless
RUN pip install pandas==2.1.1
RUN pip install Pillow==10.1.0

# Copy your code into the container
COPY facial-recognition-client facial-recognition-client

# Command to run your program
CMD ["python", "facial-recognition-client/client.py"]
