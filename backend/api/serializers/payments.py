from rest_framework import serializers
from payments.models import Transaction, Payout


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = '__all__'
