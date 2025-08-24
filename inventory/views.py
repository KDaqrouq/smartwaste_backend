from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.headless.contrib.rest_framework.authentication import XSessionTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import InventoryItem
from .serializers import InventoryItemSerializer

from datetime import date, timedelta

from fcm_django.models import FCMDevice
from smartwaste_backend.utils.firebase import send_push_v1

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
def inventory_create_read(request):
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

    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT', 'DELETE'])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def inventory_update_delete(request, pk):
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

    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def expiring_soon(request):
    today = date.today()
    three_days = today + timedelta(days=3)

    expiring_items = InventoryItem.objects.filter(user=request.user, expiry_date__gte=today,
                                                  expiry_date__lte=three_days)
    serializer = InventoryItemSerializer(expiring_items, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def fcm_token(request):
    token = request.data.get("token")
    device_type = request.data.get("device_type", "android").lower()

    if not token:
        return Response({"error": "Token required"}, status=400)

    if device_type not in ["android", "ios"]:
        return Response({"error": "Invalid device_type, must be 'android' or 'ios'"}, status=400)

    device, created = FCMDevice.objects.update_or_create(
        registration_id=token,
        defaults={
            "type": device_type,
            "user": request.user,
        },
    )
    return Response({"success": True})


@api_view(["GET"])
# make auth here for cron job
def notify_expiring_soon(request):
    today = date.today()
    three_days = today + timedelta(days=3)

    # Group items by user
    users_with_expiring = {}
    items = InventoryItem.objects.filter(
        expiry_date__gte=today,
        expiry_date__lte=three_days
    ).select_related("user")

    for item in items:
        users_with_expiring.setdefault(item.user, []).append(item)

    # Send notifications
    for user, items_list in users_with_expiring.items():
        item_names = ", ".join(i.name for i in items_list)
        message = f"Expiring soon: {item_names}"

        for device in FCMDevice.objects.filter(user=user):
            send_push_v1(device.registration_id, "Expiry Reminder", message)

    return Response({"success": True, "users_notified": len(users_with_expiring)})


@api_view(["GET"])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@permission_classes([permissions.IsAuthenticated])
def analytics_summary(request):
    items = InventoryItem.objects.filter(user=request.user)

    data = {
        "total_items": items.count(),
        "expired": items.filter(status="EX").count(),
        "used": items.filter(status="US").count(),
        "thrown": items.filter(status="TH").count(),
    }
    return Response(data)

@api_view(['GET'])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def analytics_score(request):
    items = InventoryItem.objects.filter(user=request.user)
    items_expired_count = items.filter(status = "EX").count()
    items_used_count = items.filter(status="US").count()
    items_thrown_count = items.filter(status="TH").count()

    wasted_items = items_expired_count + items_thrown_count
    total_considered = wasted_items + items_used_count

    if total_considered == 0:
        sustainability_score = 0
    else:
        sustainability_score = (items_used_count / total_considered) * 100

    return Response({"sustainability_score": round(sustainability_score, 2)})
