from django.urls import path
from .views import (YourOwnAPIView, inventory_create_read, inventory_update_delete,
                    expiring_soon, fcm_token, notify_expiring_soon,
                    analytics_summary, analytics_score,
                    ai_recommendations,
                    items_lookup)

urlpatterns = [
    path('protected/', YourOwnAPIView.as_view()),

    path('', inventory_create_read),
    path('<int:pk>/', inventory_update_delete),

    path('expiring/items/', expiring_soon),
    path('fcm/token/', fcm_token),
    path('expiring/notify/', notify_expiring_soon),

    path('analytics/summary/', analytics_summary),
    path('analytics/sustainability-score/', analytics_score),
    path('ai/recommendations/', ai_recommendations),
    path('items/lookup/', items_lookup)
]

