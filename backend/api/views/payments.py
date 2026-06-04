from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from payments.models import Transaction, Payout
from api.serializers.payments import TransactionSerializer, PayoutSerializer
from api.permissions import IsAdmin


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
