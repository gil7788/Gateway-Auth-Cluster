FROM python:3.8-slim-buster
LABEL authors="gil"

# Create app directory
RUN mkdir -p /home/app/web
WORKDIR /home/app/web

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT=production

# Install dependencies
RUN apt-get update && apt-get -y install netcat gcc && apt-get clean
RUN pip install --upgrade pip
RUN pip install -U setuptools

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Create a user and change ownership
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /home/app
USER app

# Start Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
