from rest_framework import serializers

from .models import Order, TicketTier

class PurchaseTicketSerializer(serializers.Serializer):
    event_id = serializers.UUIDField()
    tier_id = serializers.UUIDField()
    quantity = serializers.IntegerField()

class TicketTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTier
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
