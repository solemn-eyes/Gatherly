from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from organizers.models import Organizer
from api.serializers.organizers import OrganizerSerializer
from api.permissions import IsOrganizer, IsAdmin


class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # allow admins to manage all organizers
        if self.request.user and getattr(self.request.user, 'role', None) == 'admin':
            return [IsAdmin()]
        return super().get_permissions()
