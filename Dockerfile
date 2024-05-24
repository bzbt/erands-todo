# Pull base image
FROM python:3.12.3-bullseye

RUN apt-get update && apt-get install -y git

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
RUN git config --global --add safe.directory /app

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Install dependencies
COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# Copy project
COPY . .
RUN pre-commit install
CMD ["python", "manage.py", "runserver", "0.0.0.0:10800"]
