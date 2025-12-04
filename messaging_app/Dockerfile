# Use an official Python runtime as the base image
FROM python:3.10

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port Django runs on
# EXPOSE 8000 
# Expose port 8000 for Django app
EXPOSE 8000  
# equivalent to using `-p 8000:8000` when running the container

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]