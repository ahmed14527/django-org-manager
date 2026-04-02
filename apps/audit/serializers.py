from rest_framework import serializers
from .models import AuditLog
from apps.accounts.serializers import UserResponseSerializer

class AuditLogSerializer(serializers.ModelSerializer):
    user_info = UserResponseSerializer(source='user', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ('id', 'organization', 'user', 'user_info', 'action', 'action_display',
                 'resource_type', 'resource_id', 'details', 'ip_address', 'user_agent', 'created_at')
        read_only_fields = ('id', 'created_at')