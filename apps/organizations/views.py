from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Organization, Membership
from .serializers import (
    OrganizationSerializer, OrganizationCreateSerializer,
    AddUserSerializer, UserInOrganizationSerializer
)
from .permissions import IsOrganizationAdmin, IsOrganizationMember
from .services import OrganizationService
from core.pagination import CustomPagination

class CreateOrganizationView(generics.CreateAPIView):
    serializer_class = OrganizationCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        organization = OrganizationService.create_organization(
            name=serializer.validated_data['org_name'],
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return Response({
            'org_id': str(organization.id)
        }, status=status.HTTP_201_CREATED)

class AddUserToOrganizationView(generics.CreateAPIView):
    serializer_class = AddUserSerializer
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    
    def post(self, request, organization_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            membership = OrganizationService.add_user_to_organization(
                organization_id=organization_id,
                admin_user=request.user,
                email=serializer.validated_data['email'],
                role=serializer.validated_data['role'],
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
            
            return Response({
                'message': 'User added successfully',
                'membership_id': str(membership.id)
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListOrganizationUsersView(generics.ListAPIView):
    serializer_class = UserInOrganizationSerializer
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        users, _ = OrganizationService.get_organization_users(organization_id)
        return users
    
    def list(self, request, *args, **kwargs):
        organization_id = self.kwargs['organization_id']
        users, total = OrganizationService.get_organization_users(
            organization_id=organization_id,
            limit=self.request.query_params.get('limit', 20),
            offset=self.request.query_params.get('offset', 0)
        )
        
        serializer = self.get_serializer(users, many=True, context={'organization_id': organization_id})
        
        return Response({
            'items': serializer.data,
            'total': total,
            'limit': int(self.request.query_params.get('limit', 20)),
            'offset': int(self.request.query_params.get('offset', 0))
        })

class SearchOrganizationUsersView(generics.ListAPIView):
    serializer_class = UserInOrganizationSerializer
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        keyword = self.request.query_params.get('q', '')
        
        if not keyword:
            return User.objects.none()
        
        return OrganizationService.search_users(organization_id, keyword)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'organization_id': self.kwargs['organization_id']})
        return Response(serializer.data)