import uuid

from django.db import models

from accounts.models import User

# Create your models here.
class Organizer(models.Model):
    PAYOUT_CHOICES = (
        ("mpesa", "Mpesa"),
        ("bank", "Bank"),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer_profile')
    payout_method = models.CharField(
        max_length=20,
        choices=PAYOUT_CHOICES,
        default="mpesa"
    )
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    mpesa_number = models.CharField(max_length=20, blank=True, null=True)
    bank_account_number = models.CharField(max_length=20, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.organization_name
    
    @property
    def total_events(self):
        return self.events.count()
    
    @property
    def total_revenue(self):
        return sum(event.revenue for event in self.events.all())
    