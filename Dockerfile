FROM python:3.11-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    chromium \
    chromium-driver

# Install Python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Set the display port for headless Chrome
ENV DISPLAY=:99

# Copy your application files
COPY . /app
WORKDIR /app

# Start your application
CMD ["streamlit", "run", "app.py"]
