from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.headless.contrib.rest_framework.authentication import XSessionTokenAuthentication
from rest_framework.permissions import IsAuthenticated

class YourOwnAPIView(APIView):
    authentication_classes = [XSessionTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Hello, {request.user.email}! You are authenticated."
        })