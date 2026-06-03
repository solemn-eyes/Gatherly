from django.conf import settings
from django.db import models

# Create your models here.
class Notification(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=50
    )

    channel = models.CharField(
        max_length=20
    )

    status = models.CharField(
        max_length=20
    )

    payload = models.JSONField()

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )
