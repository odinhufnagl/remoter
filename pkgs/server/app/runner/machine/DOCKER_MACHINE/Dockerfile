FROM python:3.12-slim

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG TMP_FOLDER



# Install required system packages (if any).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory.
WORKDIR /app

# Copy your package and dependencies.
# Assume your package (remoter) and remote_runner.py are in the current directory.
#COPY remoter/ ./remoter/
COPY . .
# Copy the requirements file from the build context
COPY ${TMP_FOLDER} /tmp/

# Install the dependencies
RUN pip install -r /tmp/requirements.txt
# Install Python dependencies.
RUN pip install --upgrade pip

RUN pip install ./pkgs/remoter

RUN pip install cloudpickle

# Copy the entrypoint script.
COPY docker_entrypoint.py ./

# Set the entrypoint.
ENTRYPOINT ["python", "docker_entrypoint.py"]
