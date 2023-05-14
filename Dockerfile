FROM python:3.10

WORKDIR /app

# Install dlib and libxcb-xinerama0 dependencies
RUN apt-get update && \
    apt-get install -y build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev python3 python3-dev python3-pip python3-numpy python3-scipy python3-matplotlib libxcb-xinerama0

# Download dlib source code
RUN git clone https://github.com/davisking/dlib.git

# Build and install dlib from source
RUN cd dlib && \
    mkdir build && \
    cd build && \
    cmake .. && \
    cmake --build . --config Release && \
    make install && \
    ldconfig

# Install gunicorn and other Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Start the server
CMD ["gunicorn", "--bind", "127.0.0.1:8000", "project.wsgi:application"]
