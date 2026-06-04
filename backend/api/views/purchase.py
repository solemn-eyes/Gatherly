from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers.purchase import (
    TicketPurchaseSerializer
)
from tickets.models import (
    TicketTier,
    Order
)
from rest_framework import status


class PurchaseTicketAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = TicketPurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tier_id = serializer.validated_data["tier_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            tier = TicketTier.objects.get(id=tier_id)
        except TicketTier.DoesNotExist:
            return Response({"detail": "Ticket tier not found."}, status=status.HTTP_404_NOT_FOUND)

        total = tier.price_kes * quantity

        order = Order.objects.create(
            user=request.user,
            event=tier.event,
            subtotal_kes=total,
            total_amount_kes=total,
            platform_fee_kes=0,
            payment_method="mpesa",
            status="pending"
        )

        return Response({"order_id": order.id, "amount": total}, status=status.HTTP_201_CREATED)
    
