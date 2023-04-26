from django.db import models
from properties.models import Property
from django.conf import settings


class Reservation(models.Model):
    STATE_CHOICES = (
        ("Pd", "Pending"),
        ("Dn", "Denied"),
        ("Ex", "Expired"),
        ("Ap", "Approved"),
        ('Pc', 'Pending Cancellation'),
        ("Cc", "Canceled"),
        ("Tm", "Terminated"),
        ("Cm", "Completed"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user"
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="host"
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.PositiveIntegerField(default=0)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default="Pd")
    previous_state = models.CharField(max_length=2, choices=STATE_CHOICES, default="Pd")
