from rest_framework import permissions
from apps.organizations.models import Membership

class CanViewItem(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        organization_id = view.kwargs.get('organization_id')
        if not organization_id:
            return False
        
        return Membership.objects.filter(
            user=request.user,
            organization_id=organization_id
        ).exists()
    
    def has_object_permission(self, request, view, obj):
        # Admin can see all items, members only their own
        membership = Membership.objects.filter(
            user=request.user,
            organization_id=obj.organization_id
        ).first()
        
        if membership and membership.role == 'admin':
            return True
        
        return obj.created_by == request.user