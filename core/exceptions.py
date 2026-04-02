from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Custom exception handler for API errors."""
    
    response = exception_handler(exc, context)
    
    if response is not None:
        logger.error(f"Exception: {exc}, Context: {context}")
        
        return Response({
            'error': response.data.get('detail', str(exc)),
            'status_code': response.status_code
        }, status=response.status_code)
    
    # Handle unhandled exceptions
    logger.exception("Unhandled exception")
    return Response({
        'error': 'Internal server error',
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)