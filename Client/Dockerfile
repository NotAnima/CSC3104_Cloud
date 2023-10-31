# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY . /app

EXPOSE 5000

# Activate the virtual environment
RUN pip3 install -r requirements.txt

# Specify the command to run your Python script
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
