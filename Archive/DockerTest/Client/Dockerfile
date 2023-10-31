# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY . .

# Activate the virtual environment
RUN . cloud/bin/activate && \
  pip install -r requirements.txt

# Specify the command to run your Python script
CMD ["python", "FD_client.py"]
