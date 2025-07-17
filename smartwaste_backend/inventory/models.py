from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class InventoryItem(models.Model):
    AVAILABLE = 'AV'
    USED = 'US'
    EXPIRED = "EX"
    THROWN = "TH"
    STATUS_CHOICES = {
        USED: 'Used',
        EXPIRED: 'Expired',
        THROWN: 'Thrown',
        AVAILABLE: 'Available',
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=AVAILABLE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)