from django.db import models
from events.models import Event

# Create your models here.
class PromoCode(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_type = models.CharField(
        max_length=20
    )

    discount_value = models.IntegerField()

    max_uses = models.IntegerField()

    uses = models.IntegerField(default=0)

    expires_at = models.DateTimeField()

