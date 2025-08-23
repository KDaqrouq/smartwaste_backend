from rest_framework import serializers
from .models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ['user','created_at','updated_at']

    def validate_status(self, value):
        allowed = [InventoryItem.AVAILABLE, InventoryItem.USED, InventoryItem.EXPIRED, InventoryItem.THROWN]
        if value not in allowed:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(allowed)}"
            )
        return value