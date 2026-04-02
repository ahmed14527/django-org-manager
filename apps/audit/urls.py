from django.urls import path
from .views import ListAuditLogsView, AskAIChatbotView

urlpatterns = [
    path('<uuid:organization_id>/logs/', ListAuditLogsView.as_view(), name='audit-logs'),
    path('<uuid:organization_id>/ask/', AskAIChatbotView.as_view(), name='ask-ai'),
]