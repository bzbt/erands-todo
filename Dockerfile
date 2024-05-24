# Pull base image
FROM python:3.12.3-bullseye

RUN apt-get update && apt-get install -y git
RUN git config --global --add safe.directory /app

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
RUN pre-commit install

CMD ["python", "manage.py", "runserver", "0.0.0.0:9898"]
