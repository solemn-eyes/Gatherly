from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PurchaseTicketSerializer

# Create your views here.
class PurchaseTicketAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PurchaseTicketSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        # create order
        # create transaction
        # initiate payment

        return Response({
            "message": "Payment initiated"
        })
    