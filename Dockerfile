# Use official Python image
FROM python:3.12

# Set work directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000



ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]


