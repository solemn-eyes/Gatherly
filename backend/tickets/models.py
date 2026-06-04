from events.models import Event
import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class TicketTier(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_tiers")
    name = models.CharField(max_length=255)
    price_kes = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    sold = models.PositiveIntegerField(default=0)
    transfer_allowed = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"
    
    def clean(self):
        if self.sold > self.quantity:
            raise ValidationError("Sold tickets cannot exceed total quantity.")
        if self.valid_from >= self.valid_to:
            raise ValidationError("Tier validity dates are invalid.")
        
    @property
    def remaining(self):
        return self.quantity - self.sold
    
    @property
    def is_sold_out(self):
        return self.remaining <= 0
    

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("Failed", "Failed"),
        ("refunded", "Refunded"),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount_kes = models.PositiveBigIntegerField()
    platform_fee_kes = models.PositiveBigIntegerField()
    subtotal_kes = models.PositiveBigIntegerField()
    payment_method = models.CharField(max_length=50)
    placed_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_tickets(self):
        return sum(item.quantity for item in self.items.all())
    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["placed_at"]),
        ]

class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket_tier = models.ForeignKey(TicketTier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price_kes = models.PositiveBigIntegerField()

class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    STATUS_CHOICES = (
        ("active", "Active"),
        ("used", "Used"),
        ("cancelled", "Cancelled"),
    )
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    holder_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qr_token = models.CharField(max_length=255, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    checked_in_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["event"]),
        ]