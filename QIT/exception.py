# exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_404_NOT_FOUND:
            response.data = {
                'error': 'Not Found',
                'detail': 'The requested resource was not found on this server.'
            }
    
    return response
