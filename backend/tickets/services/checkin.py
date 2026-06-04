import jwt

from accounts.models import User
from organizers.models import Organizer
from django.conf import settings
from tickets.models import Ticket
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

def validate_ticket(token):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        ticket = Ticket.objects.get(
            id=payload["ticket_id"]
        )

        if ticket.status != "active":
            return False, "Ticket already used"

        return True, ticket

    except Exception:
        return False, "Invalid ticket"
    
def check_in_ticket(ticket):
    ticket.status = "used"
    ticket.checked_in_at = timezone.now()
    ticket.save()
    return ticket

@receiver(post_save, sender=User)
def create_organizer_profile(
    sender,
    instance,
    created,
    **kwargs
):

    if not created:
        return

    if instance.role != "organizer":
        return

    Organizer.objects.create(
        user=instance,
        organization_name=instance.username
    )