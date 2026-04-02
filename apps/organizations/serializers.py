from rest_framework import serializers
from .models import Organization, Membership, Role
from apps.accounts.models import User

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')

class OrganizationCreateSerializer(serializers.Serializer):
    org_name = serializers.CharField(max_length=255)

class AddUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=Role.choices)

class UserInOrganizationSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role')
    
    def get_role(self, obj):
        membership = obj.memberships.filter(organization_id=self.context.get('organization_id')).first()
        return membership.role if membership else None

class MembershipSerializer(serializers.ModelSerializer):
    user = UserInOrganizationSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    
    class Meta:
        model = Membership
        fields = ('id', 'user', 'organization', 'role', 'created_at')