# Use the official Python image as a base
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy other files into the container
COPY . .

# Tells wich port the app is using
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]