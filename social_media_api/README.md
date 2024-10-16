# Social Media API

A Django-based social media API that allows users to create posts, like and comment on posts, follow other users, and view profiles. The API is secured with JWT authentication and includes a live API documentation for easy testing.

## Features

- User registration and authentication using JWT tokens.
- CRUD functionality for posts (Create, Read, Update, Delete).
- Like and comment system for posts.
- Follow and unfollow functionality between users.
- Profile viewing and editing.
- API documentation using Swagger (drf-yasg).
- PostgreSQL as the database backend.
- Deployed on a local server for production testing.

## Project Setup

### Requirements

- Python 3.x
- Django 5.1.x
- PostgreSQL 17.0
- Other dependencies listed in `requirements.txt`

### Environment Variables

Before running the project, make sure to configure the following environment variables:

```bash
# Database settings
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Django settings
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=False

# Allowed Hosts (for production)
ALLOWED_HOSTS=localhost 127.0.0.1

# JWT token settings
JWT_SECRET=your_jwt_secret
