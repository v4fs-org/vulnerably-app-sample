# Use the official Python image from the Docker Hub
FROM python:3.12-slim


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY banking_app ./banking_app
COPY instance ./instance

# Expose the port the app runs on
EXPOSE 8000

CMD [ "gunicorn", "--bind", "127.0.0.1:8000", "banking_app.app:app" ]