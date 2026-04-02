from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import AuditLog
from .serializers import AuditLogSerializer
from .services import AuditService
from .ai_chatbot import AIChatbot
from apps.organizations.permissions import IsOrganizationAdmin
from core.pagination import CustomPagination

class ListAuditLogsView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        logs, _ = AuditService.get_organization_logs(organization_id)
        return logs
    
    def list(self, request, *args, **kwargs):
        organization_id = self.kwargs['organization_id']
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))
        
        logs, total = AuditService.get_organization_logs(
            organization_id=organization_id,
            limit=limit,
            offset=offset
        )
        
        serializer = self.get_serializer(logs, many=True)
        
        return Response({
            'logs': serializer.data,
            'total': total,
            'limit': limit,
            'offset': offset
        })

class AskAIChatbotView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    
    def post(self, request, organization_id):
        question = request.data.get('question')
        stream = request.data.get('stream', False)
        
        if not question:
            return Response({
                'error': 'Question is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get today's logs
        logs = AuditService.get_today_logs(organization_id)
        
        if not logs.exists():
            return Response({
                'answer': 'No activity found for today.'
            })
        
        # Ask AI
        chatbot = AIChatbot()
        answer = chatbot.ask(logs, question, stream)
        
        return Response({
            'question': question,
            'answer': answer,
            'logs_analyzed': logs.count()
        })