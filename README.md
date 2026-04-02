# Multi-Tenant Organization Manager

A production-ready, secure, async multi-tenant backend service built with Django REST Framework, PostgreSQL, and JWT authentication.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Security](#security)
- [Testing](#testing)
- [Deployment](#deployment)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Overview

The Multi-Tenant Organization Manager is a robust backend system designed for managing multiple organizations, users, roles, and resources. It provides secure authentication, role-based access control, audit logging, and full-text search capabilities. The system is built with a focus on security, scalability, and clean architecture principles.

### Use Cases

- **SaaS Platforms**: Manage multiple customer organizations
- **Enterprise Systems**: Handle departments as organizations
- **Project Management**: Organize teams and projects
- **Resource Management**: Track items and activities across organizations

## ✨ Features

### Core Features

- ✅ **Multi-tenancy**: Complete isolation between organizations
- ✅ **JWT Authentication**: Secure token-based authentication
- ✅ **RBAC Authorization**: Admin/Member role-based access control
- ✅ **Full-Text Search**: PostgreSQL-powered search across users and items
- ✅ **Audit Logging**: Track all actions with detailed metadata
- ✅ **Activity Insights**: AI-powered chatbot for organizational analytics
- ✅ **Docker Support**: One-command deployment with docker-compose

### Security Features

- 🔒 Password hashing with bcrypt
- 🔒 JWT tokens with configurable expiration
- 🔒 Organization-level data isolation
- 🔒 Role-based permission system
- 🔒 SQL injection protection via ORM
- 🔒 CORS configuration for API security
- 🔒 Input validation and sanitization

### API Endpoints

#### Authentication

| Method | Endpoint              | Description             |
| ------ | --------------------- | ----------------------- |
| POST   | `/api/auth/register/` | Register new user       |
| POST   | `/api/auth/login/`    | Login and get JWT token |
| GET    | `/api/auth/profile/`  | Get user profile        |

#### Organizations

| Method | Endpoint                                | Description         | Access        |
| ------ | --------------------------------------- | ------------------- | ------------- |
| POST   | `/api/organizations/`                   | Create organization | Authenticated |
| POST   | `/api/organizations/{id}/users/`        | Add user to org     | Admin only    |
| GET    | `/api/organizations/{id}/users/list/`   | List org users      | Admin only    |
| GET    | `/api/organizations/{id}/users/search/` | Search users        | Admin only    |

#### Items

| Method | Endpoint                    | Description | Access     |
| ------ | --------------------------- | ----------- | ---------- |
| POST   | `/api/items/{org_id}/`      | Create item | Member+    |
| GET    | `/api/items/{org_id}/list/` | List items  | Role-based |

#### Audit & Analytics

| Method | Endpoint                    | Description      | Access     |
| ------ | --------------------------- | ---------------- | ---------- |
| GET    | `/api/audit/{org_id}/logs/` | Get audit logs   | Admin only |
| POST   | `/api/audit/{org_id}/ask/`  | AI chatbot query | Admin only |

## 🛠 Technology Stack

### Backend

- **Python 3.11+**: Core programming language
- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14**: API framework
- **PostgreSQL 15**: Primary database
- **JWT**: Authentication (Simple JWT)
- **Gunicorn**: WSGI HTTP Server

### Database & Search

- **PostgreSQL 15**: Primary database with JSONB support
- **PostgreSQL Full-Text Search**: For efficient searching
- **Connection Pooling**: Optimized database connections

### DevOps & Deployment

- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Git**: Version control

### Development Tools

- **pytest**: Testing framework
- **drf-yasg**: API documentation (Swagger/ReDoc)
- **python-dotenv**: Environment configuration

## 🏗 Architecture

### Clean Architecture Layers

┌─────────────────────────────────────────────┐
│ Presentation Layer │
│ (Views, Serializers, URLs) │
├─────────────────────────────────────────────┤
│ Business Logic Layer │
│ (Services, Utils) │
├─────────────────────────────────────────────┤
│ Data Access Layer │
│ (Models, Repositories) │
├─────────────────────────────────────────────┤
│ Infrastructure │
│ (Database, Cache, External APIs) │
└─────────────────────────────────────────────┘

### Multi-Tenancy Design

User → Membership → Organization ← Items ← AuditLogs
↓
Role (Admin/Member)

### Request Flow

Client Request → Middleware → Authentication → Authorization
→ Business Logic → Database → Response → Audit Logging

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**

```bash
git clone https://github.com/ahmed14527/django-org-manager.git
cd django-org-manager


Configure environment variables

bash
cp .env.example .env
# Edit .env with your configuration
Start the application

bash
docker-compose up -d
Run migrations

bash
docker-compose exec web python manage.py migrate
Create superuser

bash
docker-compose exec web python manage.py createsuperuser
Access the application

API: http://localhost:8000

Admin: http://localhost:8000/admin

API Docs: http://localhost:8000/swagger/

Option 2: Local Development
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Set up PostgreSQL database

bash
# Using Docker for database only
docker run -d \
  --name postgres-dev \
  -e POSTGRES_DB=org_manager \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:15
Configure environment

bash
cp .env.example .env
# Update DATABASE_URL in .env
Run migrations

bash
python manage.py migrate
Create superuser

bash
python manage.py createsuperuser
Start development server

bash
python manage.py runserver
📚 API Documentation
Authentication Flow
1. Register User
bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "SecurePass123!"
  }'
Response:

json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
2. Login
bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
Organization Management
Create Organization
bash
curl -X POST http://localhost:8000/api/organizations/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Acme Corporation"
  }'
Response:

json
{
  "org_id": "550e8400-e29b-41d4-a716-446655440000"
}
Add User to Organization (Admin Only)
bash
curl -X POST http://localhost:8000/api/organizations/{org_id}/users/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "role": "member"
  }'
List Organization Users (Admin Only)
bash
curl -X GET "http://localhost:8000/api/organizations/{org_id}/users/list/?limit=20&offset=0" \
  -H "Authorization: Bearer <admin_token>"
Response:

json
{
  "items": [
    {
      "id": "user-id-1",
      "email": "admin@example.com",
      "full_name": "Admin User",
      "role": "admin"
    },
    {
      "id": "user-id-2",
      "email": "member@example.com",
      "full_name": "Member User",
      "role": "member"
    }
  ],
  "total": 2,
  "limit": 20,
  "offset": 0
}
Search Users (Admin Only)
bash
curl -X GET "http://localhost:8000/api/organizations/{org_id}/users/search/?q=john" \
  -H "Authorization: Bearer <admin_token>"
Item Management
Create Item
bash
curl -X POST http://localhost:8000/api/items/{org_id}/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "item_details": {
      "name": "Project Alpha",
      "description": "Initial project setup",
      "priority": "high",
      "status": "in_progress"
    }
  }'
Response:

json
{
  "item_id": "550e8400-e29b-41d4-a716-446655440000"
}
List Items (Role-based)
bash
curl -X GET "http://localhost:8000/api/items/{org_id}/list/?limit=20&offset=0" \
  -H "Authorization: Bearer <your_token>"
Response for Members:

json
{
  "items": [
    {
      "id": "item-1",
      "details": {"name": "My Item"},
      "created_by": "current_user_id",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
Response for Admins:

json
{
  "items": [
    {
      "id": "item-1",
      "details": {"name": "User 1 Item"},
      "created_by": "user1_id",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "item-2",
      "details": {"name": "User 2 Item"},
      "created_by": "user2_id",
      "created_at": "2024-01-15T11:00:00Z"
    }
  ],
  "total": 2,
  "limit": 20,
  "offset": 0
}
Audit & Analytics
Get Audit Logs (Admin Only)
bash
curl -X GET "http://localhost:8000/api/audit/{org_id}/logs/?limit=50&offset=0" \
  -H "Authorization: Bearer <admin_token>"
Response:

json
{
  "logs": [
    {
      "id": "log-1",
      "user_info": {
        "email": "admin@example.com",
        "full_name": "Admin User"
      },
      "action": "create",
      "action_display": "Create",
      "resource_type": "item",
      "details": {"name": "Project Alpha"},
      "ip_address": "192.168.1.1",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
AI Chatbot Query (Admin Only)
bash
curl -X POST http://localhost:8000/api/audit/{org_id}/ask/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many items were created today?",
    "stream": false
  }'
Response:

json
{
  "question": "How many items were created today?",
  "answer": "Based on today's audit logs, 5 items were created between 09:00 and 17:00.",
  "logs_analyzed": 25
}
📊 Database Schema
Entity Relationship Diagram
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│    User     │     │  Membership  │     │  Organization  │
├─────────────┤     ├──────────────┤     ├────────────────┤
│ id (PK)     │────<│ user_id (FK) │     │ id (PK)        │
│ email       │     │ org_id (FK)  │>────│ name           │
│ full_name   │     │ role         │     │ is_active      │
│ password    │     │ created_at   │     │ search_vector  │
│ is_active   │     └──────────────┘     │ created_at     │
│ created_at  │          │               │ updated_at     │
│ updated_at  │          │               └────────────────┘
└─────────────┘          │                      │
         │               │                      │
         │               │                      │
         │        ┌──────▼──────┐               │
         │        │    Item     │               │
         │        ├─────────────┤               │
         └───────>│ id (PK)     │               │
                  │ org_id (FK) │>──────────────┘
                  │ created_by  │
                  │ details     │
                  │ created_at  │
                  │ updated_at  │
                  └─────────────┘
                         │
                         │
                  ┌──────▼──────┐
                  │  AuditLog   │
                  ├─────────────┤
                  │ id (PK)     │
                  │ org_id (FK) │>──┐
                  │ user_id (FK)│>──┤
                  │ action      │   │
                  │ resource_type│   │
                  │ details     │   │
                  │ ip_address  │   │
                  │ created_at  │   │
                  └─────────────┘   │
                                    │
                           ┌────────┴────────┐
                           │  Organization   │
                           └─────────────────┘
Indexes for Performance
sql
-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Organizations
CREATE INDEX idx_organizations_name ON organizations(name);
CREATE INDEX idx_organizations_search_vector ON organizations USING GIN(search_vector);

-- Memberships
CREATE INDEX idx_memberships_user_org ON memberships(user_id, organization_id);
CREATE INDEX idx_memberships_organization ON memberships(organization_id);

-- Items
CREATE INDEX idx_items_organization ON items(organization_id);
CREATE INDEX idx_items_created_by ON items(created_by);
CREATE INDEX idx_items_created_at ON items(created_at);
CREATE INDEX idx_items_org_created ON items(organization_id, created_at);

-- Audit Logs
CREATE INDEX idx_audit_organization ON audit_logs(organization_id);
CREATE INDEX idx_audit_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_org_created ON audit_logs(organization_id, created_at);
🔒 Security
Authentication & Authorization
python
# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
Role-Based Access Control
python
# Permission Classes
class IsOrganizationAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is admin of the organization
        membership = Membership.objects.get(
            user=request.user,
            organization_id=view.kwargs['organization_id']
        )
        return membership.role == 'admin'

class IsOrganizationMember(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is member of the organization
        return Membership.objects.filter(
            user=request.user,
            organization_id=view.kwargs['organization_id']
        ).exists()
Data Isolation
python
# Organization-level filtering
def get_queryset(self):
    organization_id = self.kwargs['organization_id']

    # Users can only access their organization's data
    if self.request.user.is_admin:
        return Item.objects.filter(organization_id=organization_id)
    else:
        return Item.objects.filter(
            organization_id=organization_id,
            created_by=self.request.user
        )
Security Headers
python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
🧪 Testing
Running Tests
bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps tests/

# Run specific test file
pytest tests/test_accounts.py

# Run specific test
pytest tests/test_accounts.py::test_user_registration
Test Structure
python
# Example test
import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User

@pytest.mark.django_db
class TestAuthentication:
    def test_user_registration(self, api_client):
        response = api_client.post('/api/auth/register/', {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'password': 'SecurePass123!'
        })
        assert response.status_code == 201
        assert 'access_token' in response.data

    def test_user_login(self, test_user):
        response = api_client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'SecurePass123!'
        })
        assert response.status_code == 200
Test Coverage
✅ Authentication (register, login, token validation)

✅ RBAC (admin/member permissions)

✅ Organization isolation

✅ Item CRUD operations

✅ Audit logging

✅ Search functionality

✅ Error handling

🚢 Deployment
Production Configuration
Environment Variables

bash
# Production .env
SECRET_KEY=<generate_secure_key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
DB_PASSWORD=<secure_password>
ACCESS_TOKEN_LIFETIME_MINUTES=15
Database Optimization

sql
-- Configure PostgreSQL for production
ALTER SYSTEM SET max_connections = '200';
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = '0.9';
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = '100';
Gunicorn Configuration

python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
threads = 2
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
Nginx Reverse Proxy

nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
Docker Production Deployment
bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser
Monitoring & Logging
python
# logging configuration
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/app.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
⚡ Performance Optimization
Database Optimization
Query Optimization

python
# Use select_related for foreign keys
items = Item.objects.select_related('organization', 'created_by').all()

# Use only() for specific fields
users = User.objects.only('id', 'email', 'full_name')

# Use defer() to exclude large fields
logs = AuditLog.objects.defer('details').all()
Caching Strategy

python
from django.core.cache import cache

def get_organization_users(org_id):
    cache_key = f'org_users_{org_id}'
    users = cache.get(cache_key)

    if not users:
        users = Membership.objects.filter(organization_id=org_id)
        cache.set(cache_key, users, 300)  # Cache for 5 minutes

    return users
Pagination

python
# Always use pagination for list endpoints
class CustomPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
Connection Pooling
python
# Database connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Keep connections alive for 10 minutes
        'POOL_SIZE': 20,
        'MAX_OVERFLOW': 10,
    }
}
🔧 Troubleshooting
Common Issues and Solutions
1. Database Connection Issues
bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
2. Migration Errors
bash
# Reset migrations
python manage.py migrate --fake
python manage.py makemigrations
python manage.py migrate

# View migration SQL
python manage.py sqlmigrate app_name migration_name
3. Permission Denied
bash
# Fix file permissions
sudo chown -R 1000:1000 .
sudo chmod -R 755 .

# Check Docker permissions
sudo usermod -aG docker $USER
4. Token Issues
python
# Clear expired tokens
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
BlacklistedToken.objects.all().delete()
5. Slow Queries
sql
-- Identify slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
🤝 Contributing
Development Workflow
Fork the repository

Create a feature branch

bash
git checkout -b feature/amazing-feature
Make changes and commit

bash
git commit -m 'Add amazing feature'
Run tests

bash
pytest
flake8 apps/
black apps/
Push to branch

bash
git push origin feature/amazing-feature
Open a Pull Request

Coding Standards
Follow PEP 8 guidelines

Write docstrings for all functions

Add type hints where possible

Write tests for new features

Keep functions small and focused

Git Commit Convention
text
feat: Add new feature
fix: Bug fix
docs: Documentation update
style: Code style update
refactor: Code refactoring
test: Test updates
chore: Maintenance tasks
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.




🗺 Roadmap
Version 1.0 (Current)
 Multi-tenancy support

 JWT authentication

 RBAC authorization

 Full-text search

 Audit logging

 Docker deployment


```
