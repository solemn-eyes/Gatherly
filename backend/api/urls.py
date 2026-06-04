from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.views.publicevent import PublicEventViewSet
from events.views import EventViewSet
from api.views.purchase import PurchaseTicketAPIView
from api.views.mpesa import MpesaCallbackAPIView
from api.views.organizers import OrganizerViewSet
from api.views.payments import TransactionViewSet, PayoutViewSet
from api.views.promocode import PromoCodeViewSet
from api.views.notifications import NotificationViewSet

router = DefaultRouter()
router.register(r'public/events', PublicEventViewSet, basename='public-events')
router.register(r'events', EventViewSet, basename='events')
router.register(r'organizers', OrganizerViewSet, basename='organizers')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'payouts', PayoutViewSet, basename='payouts')
router.register(r'promocodes', PromoCodeViewSet, basename='promocodes')
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
    path('purchase/', PurchaseTicketAPIView.as_view(), name='purchase'),
    path('mpesa/callback/', MpesaCallbackAPIView.as_view(), name='mpesa-callback'),
]
