from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from api.serializers.notifications import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # users can only see their notifications
        user = self.request.user
        return Notification.objects.filter(user=user)
