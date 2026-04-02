from rest_framework import permissions
from .models import Membership, Role

class IsOrganizationAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        organization_id = view.kwargs.get('organization_id') or view.kwargs.get('pk')
        if not organization_id:
            return False
        
        try:
            membership = Membership.objects.get(
                user=request.user,
                organization_id=organization_id
            )
            return membership.role == Role.ADMIN
        except Membership.DoesNotExist:
            return False

class IsOrganizationMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        organization_id = view.kwargs.get('organization_id') or view.kwargs.get('pk')
        if not organization_id:
            return False
        
        return Membership.objects.filter(
            user=request.user,
            organization_id=organization_id
        ).exists()