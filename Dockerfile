# Use official Python image
FROM python:3.11-slim

# Create app directory
WORKDIR /usr/src/app

# Copy requirements.txt
COPY requirements.txt ./

# Install app dependencies
RUN pip install "uv~=0.2.2" && uv pip install --system --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch
RUN uv pip install --system --no-cache-dir -r requirements.txt
