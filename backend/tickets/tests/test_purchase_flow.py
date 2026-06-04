from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User
from organizers.models import Organizer
from events.models import Event
from tickets.models import TicketTier, Order
from django.utils import timezone
from datetime import timedelta


class PurchaseFlowTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # create attendee user
        self.user = User.objects.create_user(
            username='attendee1', email='attendee@example.com', password='pass1234'
        )

        # create organizer user and profile
        self.org_user = User.objects.create_user(
            username='org1', email='org@example.com', password='pass1234', role='organizer'
        )
        self.organizer = Organizer.objects.create(user=self.org_user, organization_name='Org 1')

        # create event
        now = timezone.now()
        self.event = Event.objects.create(
            organizer=self.organizer,
            title='Test Event',
            start_time=now + timedelta(days=2),
            end_time=now + timedelta(days=3),
            total_capacity=100,
            sales_open=now - timedelta(days=1),
            sales_close=now + timedelta(days=1),
            slug='test-event'
        )

        # create ticket tier
        self.tier = TicketTier.objects.create(
            event=self.event,
            name='General',
            price_kes=1000,
            quantity=50,
            valid_from=now - timedelta(days=2),
            valid_to=now + timedelta(days=10)
        )

    def test_purchase_creates_order(self):
        # authenticate
        self.client.force_authenticate(self.user)

        resp = self.client.post('/api/purchase/', {
            'tier_id': str(self.tier.id),
            'quantity': 2
        }, format='json')

        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertIn('order_id', data)
        self.assertIn('amount', data)

        order = Order.objects.get(id=data['order_id'])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.event, self.event)
        self.assertEqual(order.total_amount_kes, self.tier.price_kes * 2)
