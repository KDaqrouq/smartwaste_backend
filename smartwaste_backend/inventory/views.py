from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.headless.contrib.rest_framework.authentication import XSessionTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import InventoryItem
from .serializers import InventoryItemSerializer

class YourOwnAPIView(APIView):
    authentication_classes = [XSessionTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Hello, {request.user.email}! You are authenticated."
        })

@api_view(['GET', 'POST'])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def inventory_list_create(request):
    if request.method == 'GET':
        items = InventoryItem.objects.filter(user=request.user)
        serializer = InventoryItemSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk, user=request.user)

    if request.method == 'PUT':
        serializer = InventoryItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)