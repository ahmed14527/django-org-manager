from django.db import transaction
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import Organization, Membership, Role
from apps.audit.models import AuditLog, ActionType
from apps.accounts.models import User

class OrganizationService:
    
    @staticmethod
    @transaction.atomic
    def create_organization(name, user, ip_address=None, user_agent=None):
        """Create organization and assign admin role to creator."""
        organization = Organization.objects.create(name=name)
        
        membership = Membership.objects.create(
            user=user,
            organization=organization,
            role=Role.ADMIN
        )
        
        AuditLog.objects.create(
            organization=organization,
            user=user,
            action=ActionType.CREATE,
            resource_type='organization',
            resource_id=str(organization.id),
            details={'name': name},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return organization
    
    @staticmethod
    @transaction.atomic
    def add_user_to_organization(organization_id, admin_user, email, role, ip_address=None, user_agent=None):
        """Add user to organization (admin only)."""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValueError("User not found")
        
        if Membership.objects.filter(user=user, organization_id=organization_id).exists():
            raise ValueError("User is already a member of this organization")
        
        membership = Membership.objects.create(
            user=user,
            organization_id=organization_id,
            role=role
        )
        
        AuditLog.objects.create(
            organization_id=organization_id,
            user=admin_user,
            action=ActionType.INVITE,
            resource_type='membership',
            resource_id=str(membership.id),
            details={'user_email': email, 'role': role},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return membership
    
    @staticmethod
    def get_organization_users(organization_id, limit=20, offset=0):
        """Get all users in organization with pagination."""
        users = User.objects.filter(
            memberships__organization_id=organization_id
        ).distinct()
        
        total = users.count()
        users = users[offset:offset+limit]
        
        return users, total
    
    @staticmethod
    def search_users(organization_id, keyword, limit=20):
        """Search users in organization using full-text search."""
        from django.contrib.postgres.search import SearchVector
        
        users = User.objects.filter(
            memberships__organization_id=organization_id
        ).annotate(
            search=SearchVector('email', 'full_name')
        ).filter(search=keyword)
        
        return users[:limit]