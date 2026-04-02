import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from apps.audit.models import AuditLog

logger = logging.getLogger(__name__)

class AuditMiddleware(MiddlewareMixin):
    """Middleware to audit user actions."""
    
    def process_request(self, request):
        request.start_time = now()
        return None

class TenantMiddleware(MiddlewareMixin):
    """Middleware to handle multi-tenancy."""
    
    def process_request(self, request):
        # Extract organization ID from URL or headers
        path = request.path
        if '/organizations/' in path:
            parts = path.split('/')
            for i, part in enumerate(parts):
                if part == 'organizations' and i + 1 < len(parts):
                    org_id = parts[i + 1]
                    request.organization_id = org_id
                    break
        
        return None