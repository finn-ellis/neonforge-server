# backend.Dockerfile
# Use the official Python Alpine image
FROM python:3.13.7-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY ../requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .
RUN mkdir -p FileServer KioskQueue
COPY KioskQueue/kiosk_queue KioskQueue/
COPY KioskQueue/__init__.py KioskQueue/
COPY FileServer/file_server FileServer/
COPY FileServer/__init__.py FileServer/

# Boot
COPY boot.sh .
RUN chmod +x boot.sh
ENV FLASK_APP=neonforge.py

# Expose the port the app runs on (for documentation and inter-container communication)
EXPOSE 5000

# Command to run the Flask application
CMD ["./boot.sh"]