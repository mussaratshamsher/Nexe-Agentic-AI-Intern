FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port FastAPI will run on
# Hugging Face Spaces use port 7860 by default
EXPOSE 7860

# Command to run the application
# We initialize the database first, then start the server
CMD python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 7860
