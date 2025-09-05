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

from google import genai
from django.conf import settings

import requests

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

@api_view(['GET'])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def filter_category(request):
    category = request.GET.get("category")
    items = InventoryItem.objects.filter(user=request.user)

    if category:
        items = items.filter(category=category)

    return Response({"items": list(items.values())})

@api_view(['POST'])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def ai_recommendations(request):
    user = request.user
    items = InventoryItem.objects.filter(user=user)

    STATUS_MAP = {
        "AV": "Available",
        "US": "Used",
        "EX": "Expired",
        "TH": "Thrown"
    }

    history = []
    for item in items:
        history.append({
            "item": item.product_name,
            "status": STATUS_MAP.get(item.status, item.status),
            "quantity": item.quantity,
            "expiry_date": item.expiry_date.strftime("%Y-%m-%d"),
        })

    prompt = f"""
    Here is the food waste history for a user:

    {history}

    Please provide your analysis in strict JSON format **exactly like this**:

    {{
      "frequent_waste": ["Item1", "Item2"],
      "suggestions": ["Suggestion1", "Suggestion2"],
      "purchase_habits": ["Habit1", "Habit2"]
    }}

    Where:
    - "frequent_waste" is a list of the items most frequently wasted.
    - "suggestions" a list of actionable, short-term steps the user can take to reduce waste with their current items (e.g., storage tips, portion adjustments, alternative uses).
    - "purchase_habits" a list of long-term, future-oriented shopping recommendations based on the user's history (e.g., buy smaller packs, switch to frozen alternatives, avoid bulk purchases).
    
    Make sure:
    - "suggestions" focus on **what to do now** with existing food.
    - "purchase_habits" focus on **what to buy differently next time**.
    - Keep lists practical, concise, and user-friendly.
    
    Make each of these recommendations no more than 3 items each and no longer than 15 words per item.
    
    **Important:** Only output valid JSON. Do not include any explanations or extra text.
    """

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
    )

    return Response({
        "ai_suggestions": response.text
    })


@api_view(['POST'])
@authentication_classes([XSessionTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def eat_me_first(request):
    user = request.user
    items = InventoryItem.objects.filter(user=user)

    STATUS_MAP = {
        "AV": "Available",
        "US": "Used",
        "EX": "Expired",
        "TH": "Thrown"
    }

    history = []
    for item in items:
        history.append({
            "item": item.product_name,
            "status": STATUS_MAP.get(item.status, item.status),
            "quantity": item.quantity,
            "expiry_date": item.expiry_date.strftime("%Y-%m-%d"),
        })

    prompt = f"""
    Here is the food waste history for a user:

    {history}

    """

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )

    return Response({
        "ai_suggestions": response.text
    })

OFF_URL_TMPL = "https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

def normalize_off(barcode, prod: dict):
    nutr = prod.get("nutriments", {}) or {}
    def g(key):
        try:
            return float(nutr.get(key)) if nutr.get(key) is not None else None
        except ValueError:
            return None

    kcal = g("energy-kcal_100g")
    if kcal is None and g("energy_100g") is not None:
        try:
            kcal = float(nutr["energy_100g"]) / 4.184
        except Exception:
            kcal = None

    return {
        "barcode": barcode,
        "name": prod.get("product_name") or "Unknown item",
        "brand": (prod.get("brands") or "").split(",")[0].strip() if prod.get("brands") else "",
        "quantity": prod.get("quantity") or "",
        "images": [prod.get("image_front_url")] if prod.get("image_front_url") else [],
        "nutrients": {
            "per": "100 g",
            "energy_kcal": kcal,
            "protein_g": g("proteins_100g"),
            "fat_g": g("fat_100g"),
            "carbohydrates_g": g("carbohydrates_100g"),
            "sugars_g": g("sugars_100g"),
            "sodium_mg": (g("sodium_100g") * 1000) if g("sodium_100g") else None,
        },
        "ingredients": prod.get("ingredients_text", "").split(", "),
        "allergens": [a.split(":")[-1] for a in (prod.get("allergens_tags") or [])],
        "categories": [c.split(":")[-1] for c in (prod.get("categories_tags") or [])],
        "source": "open_food_facts",
    }

@api_view(["POST"])
def item_lookup(request):
    code = request.data.get("barcode")
    if not code or not code.isdigit():
        return Response({"detail": "Invalid barcode"}, status=status.HTTP_400_BAD_REQUEST)

    # Query Open Food Facts
    url = OFF_URL_TMPL.format(barcode=code)
    try:
        resp = requests.get(url, timeout=6)
        if resp.status_code != 200:
            return Response({"detail": "Lookup failed"}, status=status.HTTP_502_BAD_GATEWAY)
        data = resp.json()
    except Exception:
        return Response({"detail": "External API error"}, status=status.HTTP_502_BAD_GATEWAY)

    if data.get("status") != 1:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    product = data["product"]
    normalized = normalize_off(code, product)
    return Response(normalized, status=status.HTTP_200_OK)