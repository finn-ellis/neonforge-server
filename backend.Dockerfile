# backend.Dockerfile
# Use the official Python Alpine image
FROM python:3.13.7-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY ./MainServer/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire MainServer application code into the container.
# The .dockerignore file in your root directory will automatically prevent
# the frontend folders from being included in this copy operation.
# This preserves the correct package structure for Python imports.
COPY ./MainServer .

# Expose the port the app runs on (for documentation and inter-container communication)
EXPOSE 5000

# Command to run the Flask application
# This now works because the "MainServer" package exists inside /app
CMD ["flask", "--app", "MainServer:app", "run", "--host=0.0.0.0"]