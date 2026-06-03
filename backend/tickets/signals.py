from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.tickets.models import Ticket
from backend.tickets.services.ticket_service import assign_qr
from payments.models import Transaction

@receiver(post_save, sender=Transaction)
def process_successful_payment(
    sender,
    instance,
    created,
    **kwargs
):

    if instance.status != "success":
        return

    order = instance.order

    if order.status == "paid":
        return

    order.status = "paid"
    order.save()

    for item in order.items.all():

        tier = item.tier

        tier.sold += item.quantity

        tier.save()

        for _ in range(item.quantity):

            ticket = Ticket.objects.create(
                order_item=item,
                event=order.event,
                holder_user=order.user
            )

            assign_qr(ticket)
            