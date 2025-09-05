from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class InventoryItem(models.Model):
    AVAILABLE = 'AV'
    USED = 'US'
    EXPIRED = "EX"
    THROWN = "TH"
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (USED, 'Used'),
        (EXPIRED, 'Expired'),
        (THROWN, 'Thrown'),
    ]

    FRUIT = "FR"
    VEGETABLE = "VE"
    MEAT = "MT"
    DAIRY = "DA"
    OTHER = "OT"
    CATEGORY_CHOICES = [
        (FRUIT, "Fruit"),
        (VEGETABLE, "Vegetable"),
        (MEAT, "Meat"),
        (DAIRY, "Dairy"),
        (OTHER, "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20, default="g")
    category = models.CharField(max_length=2, default=OTHER, choices=CATEGORY_CHOICES)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=AVAILABLE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)