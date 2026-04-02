from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import AuditLog, ActionType


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_link', 'organization_link', 'action_colored', 
                   'resource_type', 'resource_id_short', 'ip_address')
    list_filter = ('action', 'resource_type', 'created_at', 'organization')
    search_fields = ('user__email', 'user__full_name', 'organization__name', 
                    'resource_id', 'ip_address')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'formatted_details')
    
    fieldsets = (
        (None, {
            'fields': ('id', 'user', 'organization', 'action', 'resource_type', 
                      'resource_id', 'details')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'organization')
    
    def timestamp(self, obj):
        """Format timestamp."""
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    timestamp.short_description = 'Time'
    timestamp.admin_order_field = 'created_at'
    
    def user_link(self, obj):
        """Link to user detail page."""
        if obj.user:
            url = reverse('admin:accounts_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return '-'
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__email'
    
    def organization_link(self, obj):
        """Link to organization detail page."""
        if obj.organization:
            url = reverse('admin:organizations_organization_change', args=[obj.organization.id])
            return format_html('<a href="{}">{}</a>', url, obj.organization.name)
        return '-'
    organization_link.short_description = 'Organization'
    organization_link.admin_order_field = 'organization__name'
    
    def action_colored(self, obj):
        """Display action with color coding."""
        colors = {
            ActionType.CREATE: 'green',
            ActionType.UPDATE: 'blue',
            ActionType.DELETE: 'red',
            ActionType.INVITE: 'orange',
            ActionType.JOIN: 'purple',
            ActionType.VIEW: 'gray',
        }
        color = colors.get(obj.action, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 
                          color, obj.get_action_display())
    action_colored.short_description = 'Action'
    action_colored.admin_order_field = 'action'
    
    def resource_id_short(self, obj):
        """Shorten resource ID for display."""
        if obj.resource_id and len(obj.resource_id) > 8:
            return obj.resource_id[:8] + '...'
        return obj.resource_id
    resource_id_short.short_description = 'Resource ID'
    
    def formatted_details(self, obj):
        """Format details as pretty JSON."""
        if obj.details:
            import json
            return format_html('<pre>{}</pre>', 
                             json.dumps(obj.details, indent=2, default=str))
        return '-'
    formatted_details.short_description = 'Details (formatted)'
    
    def get_readonly_fields(self, request, obj=None):
        """Make all fields read-only for non-superusers."""
        if not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields
    
    def has_add_permission(self, request):
        """Prevent manual addition of audit logs."""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete audit logs."""
        return request.user.is_superuser
    
    def get_actions(self, request):
        """Customize available actions."""
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            # Remove delete action for non-superusers
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions
    
    actions = ['delete_old_logs']
    
    def delete_old_logs(self, request, queryset):
        """Bulk delete logs older than 30 days."""
        cutoff_date = timezone.now() - timedelta(days=30)
        old_logs = AuditLog.objects.filter(created_at__lt=cutoff_date)
        count = old_logs.count()
        old_logs.delete()
        self.message_user(request, f'{count} logs older than 30 days deleted.')
    delete_old_logs.short_description = 'Delete logs older than 30 days'
    
    class Media:
        """Custom CSS for admin interface."""
        css = {
            'all': ('admin/css/custom.css',)
        }