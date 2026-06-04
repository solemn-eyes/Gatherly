from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .serializers import EventSerializer
from api.permissions import IsOrganizer

class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer

    permission_classes = [
        IsAuthenticated,
        IsOrganizer
    ]

    def get_queryset(self):
        return Event.objects.filter(
            organizer=self.request.user.organizer_profile
        )

    def perform_create(self, serializer):
        serializer.save(
            organizer=self.request.user.organizer_profile
        )
