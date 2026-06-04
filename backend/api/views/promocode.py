from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from promocode.models import PromoCode
from api.serializers.promocode import PromoCodeSerializer
from api.permissions import IsAdmin


class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.user and getattr(self.request.user, 'role', None) == 'admin':
            return [IsAdmin()]
        return super().get_permissions()
