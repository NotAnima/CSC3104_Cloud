# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

# Copy the local directory contents into the container at /app
COPY . .

EXPOSE 5000

# Specify the command to run your Python script
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
