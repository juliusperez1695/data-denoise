# syntax=docker/dockerfile:1

FROM python:3.14.2-slim AS base

# Set the working directory in the container
WORKDIR /data-denoise

# Install Poetry and dependencies
RUN pip install poetry

# Copy only the project files needed to install dependencies first
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
# The --no-root flag prevents installing the project itself as a package at this stage
RUN poetry install --no-root

# Copy the rest of the application code
COPY src ./src

# Define the command to run the application when the container starts
# Replace 'your_app_module:app' with the actual entry point of your application
CMD ["poetry", "run", "python", "src/data_denoise_main.py"]
