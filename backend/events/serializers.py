from rest_framework import serializers
from .models import Event
from tickets.models import TicketTier

class TicketTierSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketTier
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):

    ticket_tiers = TicketTierSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Event
        fields = "__all__"
        