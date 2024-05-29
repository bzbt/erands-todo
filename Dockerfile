# Pull base image
FROM python:3.12.3-bullseye

RUN mkdir /app

RUN apt-get update && apt-get install -y git
RUN git config --global --add safe.directory /app

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN pre-commit install

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
