# Use an official Python 3.12 runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install any dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the FastAPI port
EXPOSE 8055

# Run the application
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8055"]
