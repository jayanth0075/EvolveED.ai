# tutor/urls.py
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def tutor_test(request):
    return Response({"message": "Tutor API is working"})

urlpatterns = [
    path('test/', tutor_test, name='tutor-test'),
]
