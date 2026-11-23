FROM python:3.15.2-slim-trixie

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

## Install system dependencies
RUN apt-get update && apt-get upgrade -y

# git: for git based python dependencies
RUN apt-get install -y git

# Setup local workdir and dependencies
WORKDIR /app

# Install other python dependencies.
ADD ./pyproject.toml ./pyproject.toml
RUN mkdir -p signwriting_description && touch README.md
RUN pip install --no-cache-dir ".[server]"

# Copy local code to the container image.
COPY ./signwriting_description ./signwriting_description

RUN useradd --create-home --uid 1000 app
RUN rm -rf /usr/local/lib/python*/ensurepip /usr/local/lib/python*/site-packages/pip /usr/local/lib/python*/site-packages/pip-*.dist-info /opt/venv/lib/python*/site-packages/pip /opt/venv/lib/python*/site-packages/pip-*.dist-info

USER app
ENV PORT=8080

# Run the web service on container startup. Here we use the uvicorn
# ASGI server, with one worker process.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec uvicorn signwriting_description.server:app --host 0.0.0.0 --port $PORT --workers 1
