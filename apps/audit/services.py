from django.db.models import Q
from datetime import datetime, timedelta
from .models import AuditLog

class AuditService:
    
    @staticmethod
    def get_organization_logs(organization_id, limit=50, offset=0):
        """Get audit logs for an organization."""
        logs = AuditLog.objects.filter(
            organization_id=organization_id
        ).select_related('user').order_by('-created_at')
        
        total = logs.count()
        logs = logs[offset:offset+limit]
        
        return logs, total
    
    @staticmethod
    def get_today_logs(organization_id):
        """Get today's logs for an organization."""
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        return AuditLog.objects.filter(
            organization_id=organization_id,
            created_at__gte=today,
            created_at__lt=tomorrow
        ).select_related('user').order_by('-created_at')