# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
RUN mkdir /code
WORKDIR /code

# Copy the current directory contents into the container at /app
ADD . /code

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables
ENV APP_NAME file-frontend
ENV COMMIT LOCAL
ENV FILE_API_URI http://localhost:8081
ENV LOG_LEVEL DEBUG
ENV UPLOAD_FOLDER file_frontend/temp_uploads
ENV PYTHONUNBUFFERED 1

# Run start command
CMD ["python3", "manage.py", "runserver"]
