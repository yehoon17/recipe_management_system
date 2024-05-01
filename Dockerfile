# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app
COPY website /app/website

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory to the Django project directory
WORKDIR /app/website

# Migrate
RUN python manage.py migrate

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run Django migrations and start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
