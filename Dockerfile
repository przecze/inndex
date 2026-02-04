# Use official Python image
FROM python:3.13-slim

# Create app directory
WORKDIR /usr/src/app

# Copy requirements.txt
COPY requirements.txt ./

# Install app dependencies
RUN pip install "uv~=0.9.30" && uv pip install --system --no-cache-dir -r requirements.txt
