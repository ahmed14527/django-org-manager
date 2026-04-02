# Multi-Tenant Organization Manager (Django)

A production-ready, multi-tenant organization management system built with Django REST Framework.

## Features

- **JWT Authentication** with Django REST Framework Simple JWT
- **Multi-tenancy** with organization isolation
- **RBAC** (Admin/Member roles)
- **Full-text search** with PostgreSQL
- **Audit logging** for all actions
- **AI-powered chatbot** for organizational insights
- **Dockerized** with docker-compose
- **Comprehensive tests**

## Quick Start

```bash
# Clone repository
git clone <repo-url>
cd django-org-manager

# Copy environment file
cp .env.example .env

# Start with Docker Compose
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the API at http://localhost:8000
# API documentation at http://localhost:8000/swagger/
```
