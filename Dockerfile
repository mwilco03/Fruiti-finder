# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages
RUN pip install requests blackboxprotobuf flask

# Add a non-root user and switch to it
RUN useradd -m nonrootuser
USER nonrootuser

# Make port 8080 available to the world outside this container
EXPOSE 9080

# Run the application
CMD ["python", "app.py"]
