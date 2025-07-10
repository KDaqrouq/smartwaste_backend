from django.db import models

# Create your models here.

class User(models.Model):
    pass

class InventoryItem(models.Model):
    AVAILABLE = 'AV'
    USED = 'US'
    EXPIRED = "EX"
    THROWN = "TH"
    STATUS_CHOICES = {
        USED: 'Used',
        EXPIRED: 'Expired',
        THROWN: 'Thrown',
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