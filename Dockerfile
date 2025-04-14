# Use official Python image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
