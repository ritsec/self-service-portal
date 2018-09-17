# Use the official python image for python3 - using Alpine because it's super
# small and also best practices I guess
FROM python:3-alpine

# Create working directory
WORKDIR /self-service

# Install packages required to build uWSGI
RUN apk --update add build-base linux-headers

# Install pip requirements
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip

# Configure uWSGI
COPY uwsgi.ini ./uwsgi.ini

# Run the application on startup
CMD uwsgi --ini uwsgi.ini

# Copy over application files
COPY portal ./portal