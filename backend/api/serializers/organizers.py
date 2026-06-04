from rest_framework import serializers
from organizers.models import Organizer


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'
