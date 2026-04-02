Multi-Tenant Organization Manager

A production-ready multi-tenant backend service with JWT authentication, role-based access control, and audit logging. Built with Django REST Framework and PostgreSQL.
Overview
Backend system for managing multi-tenant organizations with secure authentication, granular permissions, and activity tracking. Supports SaaS platforms, enterprise applications, and resource management systems requiring organizational isolation.
Features

Multi-tenancy – Complete data isolation between organizations
JWT Authentication – Token-based auth with configurable expiration
Role-Based Access Control – Admin/Member permissions with organization-scoped authorization
Full-Text Search – PostgreSQL-powered search across users and items
Audit Logging – Comprehensive activity tracking with metadata
AI Analytics – Chatbot interface for organizational insights (admin only)

Tech Stack
Backend

Python 3.11+, Django 4.2.7, Django REST Framework 3.14
JWT authentication (Simple JWT)
Gunicorn WSGI server

Database

PostgreSQL 15 with JSONB support
Full-text search with GIN indexes
Connection pooling

DevOps

Docker & Docker Compose
pytest for testing

Architecture
┌─────────────────────────────────────┐
│ Presentation Layer │
│ (Views, Serializers, URLs) │
├─────────────────────────────────────┤
│ Business Logic │
│ (Services, Permissions) │
├─────────────────────────────────────┤
│ Data Access │
│ (Models, QuerySets) │
├─────────────────────────────────────┤
│ Infrastructure │
│ (PostgreSQL, JWT) │
└─────────────────────────────────────┘
Multi-Tenancy Model:
User → Membership (role) → Organization ← Items, AuditLogs
Members see only their own items. Admins see all organization data.
Setup & Installation
Docker (Recommended)
bash# Clone and configure
git clone https://github.com/ahmed14527/django-org-manager.git
cd django-org-manager
cp .env.example .env

# Start services

docker-compose up -d

# Run migrations and create superuser

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
Access:

API: http://localhost:8000
Admin: http://localhost:8000/admin
Docs: http://localhost:8000/swagger/

Local Development
bash# Create virtual environment
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Install dependencies

pip install -r requirements.txt

# Start PostgreSQL (Docker)

docker run -d --name postgres-dev \
 -e POSTGRES_DB=org_manager \
 -e POSTGRES_USER=postgres \
 -e POSTGRES_PASSWORD=postgres \
 -p 5432:5432 postgres:15

# Configure and run

cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Environment Variables
bash# Core
SECRET_KEY=<generate-secure-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com

# Database

DATABASE_URL=postgresql://user:pass@host:5432/dbname

# JWT

ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=1
API Overview
Authentication
Register: POST /api/auth/register/
json{
"email": "user@example.com",
"full_name": "John Doe",
"password": "SecurePass123!"
}
Login: POST /api/auth/login/
json{
"email": "user@example.com",
"password": "SecurePass123!"
}
Returns access_token and refresh_token.
Profile: GET /api/auth/profile/ (requires Bearer token)
Organizations
EndpointMethodAccessDescription/api/organizations/POSTAuthenticatedCreate organization/api/organizations/{id}/users/POSTAdminAdd user to org/api/organizations/{id}/users/list/GETAdminList org users/api/organizations/{id}/users/search/?q=queryGETAdminSearch users
Items
EndpointMethodAccessDescription/api/items/{org_id}/POSTMember+Create item/api/items/{org_id}/list/GETRole-basedList items (members: own items, admins: all)
Create Item Example:
json{
"item_details": {
"name": "Project Alpha",
"status": "in_progress",
"priority": "high"
}
}
Audit & Analytics
EndpointMethodAccessDescription/api/audit/{org_id}/logs/GETAdminRetrieve audit logs/api/audit/{org_id}/ask/POSTAdminAI chatbot query
AI Query Example:
json{
"question": "How many items were created today?",
"stream": false
}
Full API documentation: /swagger/
Running the Project
Docker:
bashdocker-compose up -d # Start all services
docker-compose logs -f web # View logs
docker-compose exec web python manage.py <command> # Run management commands
Local:
bashpython manage.py runserver # Development server
python manage.py test # Run tests
Testing
bash# Run all tests
pytest

# With coverage

pytest --cov=apps tests/

# Specific test file

pytest tests/test_accounts.py

```

**Test coverage includes:**
- Authentication flows (register, login, token validation)
- RBAC enforcement (admin/member permissions)
- Organization data isolation
- Item CRUD operations
- Audit logging
- Search functionality

## Database Schema
```

┌─────────────┐ ┌──────────────┐ ┌────────────────┐
│ User │ │ Membership │ │ Organization │
├─────────────┤ ├──────────────┤ ├────────────────┤
│ id (PK) │────<│ user_id (FK) │ │ id (PK) │
│ email │ │ org_id (FK) │>────│ name │
│ full_name │ │ role │ │ search_vector │
│ password │ └──────────────┘ └────────────────┘
└─────────────┘ │ │
│ │ │
│ ┌──────▼───────┐ │
│ │ Item │ │
│ ├──────────────┤ │
└─────────────>│ org_id (FK) │>──────────┘
│ created_by │
│ details │
└──────────────┘
│
┌──────▼───────┐
│ AuditLog │
├──────────────┤
│ org_id (FK) │
│ user_id (FK) │
│ action │
│ details │
└──────────────┘
Key Indexes:

users.email, organizations.search_vector (GIN)
memberships(user_id, organization_id) composite
items(organization_id, created_at) for time-based queries
audit_logs(organization_id, created_at) for log retrieval

License
MIT License - see LICENSE file for details.
