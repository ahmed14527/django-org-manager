from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Item
from .serializers import ItemSerializer, ItemCreateSerializer
from .permissions import CanViewItem
from apps.audit.models import AuditLog, ActionType
from apps.organizations.models import Membership

class CreateItemView(generics.CreateAPIView):
    serializer_class = ItemCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, organization_id):
        # Check membership
        try:
            membership = Membership.objects.get(
                user=request.user,
                organization_id=organization_id
            )
        except Membership.DoesNotExist:
            return Response({
                'error': 'Not a member of this organization'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        item = Item.objects.create(
            organization_id=organization_id,
            created_by=request.user,
            details=serializer.validated_data['item_details']
        )
        
        # Create audit log
        AuditLog.objects.create(
            organization_id=organization_id,
            user=request.user,
            action=ActionType.CREATE,
            resource_type='item',
            resource_id=str(item.id),
            details=item.details,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return Response({
            'item_id': str(item.id)
        }, status=status.HTTP_201_CREATED)

class ListItemsView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, CanViewItem]
    
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        
        # Check if user is admin
        membership = Membership.objects.filter(
            user=self.request.user,
            organization_id=organization_id
        ).first()
        
        if membership and membership.role == 'admin':
            # Admin sees all items
            queryset = Item.objects.filter(organization_id=organization_id)
        else:
            # Member sees only their own items
            queryset = Item.objects.filter(
                organization_id=organization_id,
                created_by=self.request.user
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        total = queryset.count()
        items = queryset[offset:offset+limit]
        
        serializer = self.get_serializer(items, many=True)
        
        # Create audit log for viewing
        AuditLog.objects.create(
            organization_id=self.kwargs['organization_id'],
            user=request.user,
            action=ActionType.VIEW,
            resource_type='item',
            details={'viewed_items': len(items)},
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return Response({
            'items': serializer.data,
            'total': total,
            'limit': limit,
            'offset': offset
        })