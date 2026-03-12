FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    ninja-build \
    build-essential \
    nvidia-container-toolkit \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip config set global.break-system-packages true

# Set working directory
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]