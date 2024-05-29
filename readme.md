# Django 5 Todo App

A simple Todo application built with Django 5 and Python 3.12.

## Features

- User authentication and registration
- Create, update, and delete tasks
- Mark tasks as completed
- Weather data from OpenWeather API

## Prerequisites

- docker
- docker compose

## Installation

1. **Create and configure the `.env` file:**

   Create a `.env` file in the project root directory with the following content:

    ```env
    DB_HOST=etdb
    DB_NAME=etdata
    DB_USER=postgres
    DB_PASSWORD=postgres
    MIN_PASSWORD_LENGTH=8
    OPENWEATHER_API_KEY=your_openweather_api_key
    APP_SECRET_KEY=your_secret_key
    ```

   Replace `your_openweather_api_key` with your actual database credentials, OpenWeather API key, and a secret key for
   Django.

   These fields, should stay the same if you are using the docker-compose file provided.

    ```env
   DB_HOST=etdb
   DB_NAME=etdata
   DB_USER=postgres
   DB_PASSWORD=postgres
   ```
2. **Build the Docker containers:**

    ```sh
    docker compose up --build
    ```

3. **Apply migrations:**

    ```sh
    docker compose exec etweb python manage.py migrate
    ```

4. **Create a superuser:**

    ```sh
    docker compose exec etweb python manage.py createsuperuser
    ```

   Follow the prompts to create a superuser account. You can use this account to log in to
   the [admin interface](http://0.0.0.0:8000/admin).

5. **Access the application:**

   Open your web browser and go to `http://0.0.0.0:8000`.
