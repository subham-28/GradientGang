# Use official Python 3.10 slim image
FROM python:3.10-slim
# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to install dependencies first (Docker cache optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
