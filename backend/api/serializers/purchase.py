from rest_framework import serializers


class TicketPurchaseSerializer(
    serializers.Serializer
):

    tier_id = serializers.UUIDField()

    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, attrs):
        from tickets.models import TicketTier

        try:
            tier = TicketTier.objects.get(id=attrs['tier_id'])
        except TicketTier.DoesNotExist:
            raise serializers.ValidationError({"tier_id": "Ticket tier does not exist."})

        if tier.remaining < attrs['quantity']:
            raise serializers.ValidationError({"quantity": "Not enough tickets available for this tier."})

        return attrs
