from django.urls import path
from .views import YourOwnAPIView, inventory_create_read, inventory_update_delete, expiring_soon

urlpatterns = [
    path('protected/', YourOwnAPIView.as_view()),

    path('', inventory_create_read),
    path('<int:pk>/', inventory_update_delete),
    path('expiring_soon/', expiring_soon),
]

