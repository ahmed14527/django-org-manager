from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin interface for Item model with comprehensive backend features.
    """
    
    # List display configuration
    list_display = (
        'id',
        'organization_name',
        'creator_email',
        'details_preview',
        'created_at',
        'updated_at',
        'item_age'
    )
    
    # Filters for sidebar
    list_filter = (
        'created_at',
        'updated_at',
        'organization',
        'created_by',
    )
    
    # Search fields
    search_fields = (
        'id',
        'organization__name',
        'created_by__email',
        'created_by__full_name',
        'details',
    )
    
    # Default ordering
    ordering = ('-created_at',)
    
    # Read-only fields
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'formatted_details'
    )
    
    # Fieldsets for form layout
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'organization', 'created_by', 'details')
        }),
        ('Details Viewer', {
            'fields': ('formatted_details',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Performance optimizations
    raw_id_fields = ('organization', 'created_by')
    autocomplete_fields = ('organization', 'created_by')
    
    # Date hierarchy for navigation
    date_hierarchy = 'created_at'
    
    # Custom actions
    actions = [
        'export_as_csv',
        'delete_selected_items',
        'bulk_update_organization'
    ]
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('organization', 'created_by')
    
    def organization_name(self, obj):
        """Display organization name with link."""
        if obj.organization:
            url = reverse('admin:organizations_organization_change', args=[obj.organization.id])
            return format_html('<a href="{}">{}</a>', url, obj.organization.name)
        return '-'
    organization_name.short_description = 'Organization'
    organization_name.admin_order_field = 'organization__name'
    
    def creator_email(self, obj):
        """Display creator email with link."""
        if obj.created_by:
            url = reverse('admin:accounts_user_change', args=[obj.created_by.id])
            return format_html('<a href="{}">{}</a>', url, obj.created_by.email)
        return '-'
    creator_email.short_description = 'Created By'
    creator_email.admin_order_field = 'created_by__email'
    
    def details_preview(self, obj):
        """Preview item details with truncation."""
        if not obj.details:
            return '-'
        
        import json
        details_str = json.dumps(obj.details, default=str)
        
        if len(details_str) > 100:
            preview = details_str[:100] + '...'
        else:
            preview = details_str
        
        return format_html(
            '<span title="{}">{}</span>',
            details_str.replace('"', '&quot;'),
            preview
        )
    details_preview.short_description = 'Details'
    
    def formatted_details(self, obj):
        """Display formatted JSON details."""
        if not obj.details:
            return '-'
        
        import json
        try:
            formatted = json.dumps(obj.details, indent=2, default=str)
            return format_html(
                '<pre style="background-color: #f5f5f5; padding: 10px; border-radius: 4px; '
                'overflow-x: auto; font-size: 12px; font-family: monospace;">{}</pre>',
                formatted
            )
        except Exception:
            return str(obj.details)
    formatted_details.short_description = 'Formatted Details'
    
    def item_age(self, obj):
        """Display item age with color coding."""
        now = timezone.now()
        age = now - obj.created_at
        
        if age < timedelta(hours=1):
            color = '#28a745'
            label = f'{age.seconds // 60} min ago'
        elif age < timedelta(days=1):
            color = '#17a2b8'
            label = f'{age.seconds // 3600} hours ago'
        elif age < timedelta(days=7):
            color = '#ffc107'
            label = f'{age.days} days ago'
        else:
            color = '#dc3545'
            label = f'{age.days} days ago'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px;">{}</span>',
            color,
            label
        )
    item_age.short_description = 'Age'
    item_age.admin_order_field = 'created_at'
    
    def export_as_csv(self, request, queryset):
        """Export selected items as CSV file."""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="items_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Organization ID', 'Organization Name', 
            'Created By ID', 'Created By Email', 'Created By Name',
            'Details', 'Created At', 'Updated At'
        ])
        
        for item in queryset:
            writer.writerow([
                str(item.id),
                str(item.organization_id) if item.organization_id else '',
                item.organization.name if item.organization else '',
                str(item.created_by_id) if item.created_by_id else '',
                item.created_by.email if item.created_by else '',
                item.created_by.full_name if item.created_by else '',
                str(item.details),
                item.created_at.isoformat() if item.created_at else '',
                item.updated_at.isoformat() if item.updated_at else ''
            ])
        
        self.message_user(request, f'Exported {queryset.count()} items successfully.')
        return response
    export_as_csv.short_description = 'Export selected items to CSV'
    
    def delete_selected_items(self, request, queryset):
        """Delete selected items with confirmation."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Successfully deleted {count} items.')
    delete_selected_items.short_description = 'Delete selected items'
    
    def bulk_update_organization(self, request, queryset):
        """Bulk update organization for selected items."""
        from django.contrib import messages
        from django.shortcuts import redirect
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        
        if 'apply' in request.POST:
            org_id = request.POST.get('organization')
            if org_id:
                count = queryset.update(organization_id=org_id)
                self.message_user(request, f'Updated {count} items to new organization.')
                return HttpResponseRedirect(request.get_full_path())
        
        # Show intermediate page
        from django.template.response import TemplateResponse
        context = {
            'items': queryset,
            'action': 'bulk_update_organization',
            'organizations': Organization.objects.all()
        }
        return TemplateResponse(request, 'admin/bulk_update_organization.html', context)
    bulk_update_organization.short_description = 'Bulk update organization'
    
    def get_search_results(self, request, queryset, search_term):
        """Enhanced search with JSON field support."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        # Search in JSON fields
        if search_term:
            # Search in JSON field values
            json_search = Q()
            # This is a simple approach - for complex JSON search consider PostgreSQL specific features
            json_search |= Q(details__icontains=search_term)
            queryset |= self.model.objects.filter(json_search)
        
        return queryset, use_distinct
    
    def get_readonly_fields(self, request, obj=None):
        """Dynamic readonly fields based on user permissions."""
        if not request.user.is_superuser:
            # Non-superusers cannot modify these fields
            return self.readonly_fields + ('organization', 'created_by')
        return self.readonly_fields
    
    def has_add_permission(self, request):
        """Check if user can add items."""
        return True
    
    def has_change_permission(self, request, obj=None):
        """Check if user can change items."""
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Check if user can delete items."""
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        """Check if user can view items."""
        return True
    
    def get_actions(self, request):
        """Customize available actions based on user."""
        actions = super().get_actions(request)
        
        # Remove delete action for non-superusers
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        
        return actions
    
    def save_model(self, request, obj, form, change):
        """Custom save behavior."""
        if not change:  # Creating new item
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Filter queryset based on user permissions."""
        qs = super().get_queryset(request)
        
        # Non-superusers can only see items from organizations they belong to
        if not request.user.is_superuser:
            from apps.organizations.models import Membership
            user_orgs = Membership.objects.filter(
                user=request.user
            ).values_list('organization_id', flat=True)
            qs = qs.filter(organization_id__in=user_orgs)
        
        return qs.select_related('organization', 'created_by')
    
    class Media:
        """Custom CSS/JS for admin."""
        css = {
            'all': ('admin/css/item_admin.css',)
        }
        js = ('admin/js/item_admin.js',)