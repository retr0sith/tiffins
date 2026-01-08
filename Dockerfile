# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /apps

# Copy project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .



# Run FastAPI on container start
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8004"]
