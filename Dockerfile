FROM selenium/standalone-chrome

# Copy your scraping code into the container
COPY app.py /usr/src/app/

WORKDIR /usr/src/app

# Install any necessary dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install selenium

CMD ["python3", "app.py"]
