# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 7002 available to the world outside this container
EXPOSE 7002

# Define environment variable
ENV NAME OPAL Server

# Run OPAL Server
CMD ["python", "opal_server.py"]
