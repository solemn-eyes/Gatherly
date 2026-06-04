from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from events.models import Event
from tickets.models import Order
from api.permissions import IsOrganizer

# Create your views here.
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response

from tickets.models import Ticket

class OrganizerDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsOrganizer
    ]

    def get(self, request):

        organizer = request.user.organizer_profile

        events = Event.objects.filter(
            organizer=organizer
        )

        revenue = (
            Order.objects.filter(
                event__organizer=organizer,
                status="paid"
            ).aggregate(
                total=Sum("total_amount_kes")
            )
        )

        return Response({
            "total_events": events.count(),
            "total_revenue":
                revenue["total"] or 0,
            "total_attendees":
                Ticket.objects.filter(
                    event__organizer=organizer
                ).count()
        })
    