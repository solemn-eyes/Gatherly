import jwt
from datetime import datetime
from django.conf import settings

def generate_qr_token(ticket):
    payload = {
        "ticket_id": str(ticket.id),
        "event_id": str(ticket.event.id),
        "holder_id": str(ticket.holder.id),
        "tier_id": str(ticket.order_item.tier.id),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def assign_qr(ticket):
    ticket.qr_token = generate_qr_token(ticket)
    ticket.save(
        update_fields=["qr_token"]
    )
    
