from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Organization, Membership, Role


class MembershipInline(admin.TabularInline):
    """Inline admin for memberships within organization."""
    model = Membership
    extra = 1
    fields = ('user', 'role', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('user',)
    show_change_link = True


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'member_count', 'is_active', 'created_at', 'view_members_link')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'id')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'member_count')
    
    fieldsets = (
        (None, {
            'fields': ('id', 'name', 'is_active')
        }),
        ('Statistics', {
            'fields': ('member_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [MembershipInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            member_count=Count('memberships', distinct=True)
        )
    
    def member_count(self, obj):
        return obj.member_count
    member_count.short_description = 'Total Members'
    member_count.admin_order_field = 'member_count'
    
    def view_members_link(self, obj):
        """Link to view all members of this organization."""
        url = reverse('admin:organizations_membership_changelist')
        return format_html('<a href="{}?organization__id__exact={}">View Members</a>', url, obj.id)
    view_members_link.short_description = 'Members'
    view_members_link.allow_tags = True


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'created_at', 'user_link', 'org_link')
    list_filter = ('role', 'created_at', 'organization')
    search_fields = ('user__email', 'user__full_name', 'organization__name')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at')
    autocomplete_fields = ('user', 'organization')
    
    fieldsets = (
        (None, {
            'fields': ('id', 'user', 'organization', 'role')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """Link to user detail page."""
        url = reverse('admin:accounts_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__email'
    
    def org_link(self, obj):
        """Link to organization detail page."""
        url = reverse('admin:organizations_organization_change', args=[obj.organization.id])
        return format_html('<a href="{}">{}</a>', url, obj.organization.name)
    org_link.short_description = 'Organization'
    org_link.admin_order_field = 'organization__name'
    
    actions = ['make_admin', 'make_member']
    
    def make_admin(self, request, queryset):
        """Bulk action to set role to admin."""
        updated = queryset.update(role=Role.ADMIN)
        self.message_user(request, f'{updated} memberships updated to Admin.')
    make_admin.short_description = 'Set selected memberships to Admin'
    
    def make_member(self, request, queryset):
        """Bulk action to set role to member."""
        updated = queryset.update(role=Role.MEMBER)
        self.message_user(request, f'{updated} memberships updated to Member.')
    make_member.short_description = 'Set selected memberships to Member'