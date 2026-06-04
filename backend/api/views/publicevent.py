from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from events.models import Event
from events.serializers import EventSerializer


class PublicEventViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Event.objects.filter(status="published")

    serializer_class = EventSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["start_time", "created_at"]
    pagination_class = LimitOffsetPagination
