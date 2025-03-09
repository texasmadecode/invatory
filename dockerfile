# Use an official Ubuntu runtime as the base image
FROM ubuntu:18.04

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY app/ /app
COPY app/templates/ /app/templates
COPY requirements.txt /app/
COPY tests/ /app/tests

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "app.py"]