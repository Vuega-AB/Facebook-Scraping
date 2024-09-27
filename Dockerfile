FROM python:3.11-slim

# Install necessary dependencies for Selenium and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    chromium \
    chromium-driver \
    libnss3 \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    xdg-utils \
    libx11-xcb1 \
    xvfb \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Set up the virtual display for Chromium
RUN Xvfb :99 -ac &
ENV DISPLAY=:99

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Command to run the app
CMD ["streamlit", "run", "app.py"]
