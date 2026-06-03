import uuid
from tickets.models import Order
from organizers.models import Organizer
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Transaction(models.Model):
    DIRECTION_CHOICES = (
        ("charge", "Charge"),
        ("refund", "Refund"),
    )
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    provider = models.CharField(max_length=50)
    provider_reference = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="KES")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["provider_reference"]),
        ]


class Payout(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("settled", "Settled"),
        ("failed", "Failed"),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    gross_kes = models.DecimalField(max_digits=10, decimal_places=2)
    fee_kes = models.DecimalField(max_digits=10, decimal_places=2)
    net_kes = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    provider_reference = models.CharField(max_length=255, blank=True, null=True)
    initiated_at = models.DateTimeField(auto_now_add=True)
    settled_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payout {self.id} for {self.organizer.user.username} - {self.net_kes} KES"
    
    def clean(self):
        if self.net_kes != self.gross_kes - self.fee_kes:
            raise ValidationError("Net amount mismatch. Net should be Gross minus Fee.")
        

    