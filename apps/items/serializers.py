from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Item
        fields = ('id', 'organization', 'created_by', 'created_by_email', 'created_by_name',
                 'details', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

class ItemCreateSerializer(serializers.Serializer):
    item_details = serializers.JSONField()