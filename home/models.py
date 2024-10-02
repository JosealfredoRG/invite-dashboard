from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Import the User model
from django.core.validators import RegexValidator

class Event(models.Model):
    event_name = models.CharField(max_length=255, default="nombre del evento")
    event_date = models.DateField()
    ceremony_location = models.CharField(max_length=255)
    reception_location = models.CharField(max_length=255)
    ceremony_map_location = models.CharField(max_length=500, blank=True, null=True)
    reception_map_location = models.CharField(max_length=500, blank=True, null=True)
    groom_name = models.CharField(
        max_length=100,
        validators=[RegexValidator(
            regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',  # Allow Spanish letters, accents, and spaces
            message='El nombre solo puede contener letras y espacios',
            code='invalid_groom_name'
        )]
        )
    bride_name = models.CharField(
        max_length=100,
         validators=[RegexValidator(
            regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',  # Allow Spanish letters, accents, and spaces
            message='El nombre solo puede contener letras y espacios',
            code='invalid_groom_name'
        )])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    observations = models.TextField(blank=True, null=True)

    # Add the user field
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bride_name} & {self.groom_name} - {self.event_date}"

class GuestCategory(models.Model):
    category_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

class RelatedTo(models.Model):
    related_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.related_name

class Guest(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    additional_guests_amount = models.PositiveIntegerField(default=0)
    invitation_link = models.URLField(max_length=500, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests', null=True, blank=True)
    category = models.ForeignKey(GuestCategory, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    related_to = models.ForeignKey(RelatedTo, on_delete=models.SET_NULL, null=True)
    will_assist = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

