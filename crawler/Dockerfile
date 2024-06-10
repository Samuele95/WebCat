# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory files (on your machine) to the container
ADD . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .

# Expose the port server is running on
EXPOSE 8000

# Start the server
RUN ["python", "webcrawler/manage.py", "makemigrations", "webcrawlerapp"]
RUN ["python", "webcrawler/manage.py", "migrate"]
RUN ["python", "webcrawler/manage.py", "loaddata", "db.json"]
CMD ["python", "webcrawler/manage.py", "runserver", "0.0.0.0:8000"]
