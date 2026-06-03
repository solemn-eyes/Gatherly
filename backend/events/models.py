import uuid
from django.db import models
from organizers.models import Organizer
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Venue(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Event(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    VISIBILITY_CHOICES = (
        ("public", "Public"),
        ("private", "Private"),
        ("unlisted", "Unlisted"),
    )
    
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default="public")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_capacity = models.PositiveIntegerField()
    waitlist_enabled = models.BooleanField(default=False)
    sales_open = models.DateTimeField()
    sales_close = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")
        if self.sales_open >= self.sales_close:
            raise ValidationError("Sales open time must be before sales close time.")
        if self.sales_close >= self.start_time:
            raise ValidationError("Tickets sales must close before the event starts.")
        
    @property
    def tickets_sold(self):
        return sum(tier.sold for tier in self.ticket_tiers.all())
    
    @property
    def tickets_remaining(self):
        return self.total_capacity - self.tickets_sold
    
    @property
    def is_sold_out(self):
        return self.tickets_remaining <= 0
    
    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["visibility"]),
            models.Index(fields=["category"]),
            models.Index(fields=["start_time"]),
        ]
    