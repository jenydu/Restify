from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import ReservationNotification
from reservations.models import Reservation
from datetime import datetime, timedelta

@receiver(post_save, sender=Reservation)
def create_reservation_notification(sender, instance, created, **kwargs):
    propty = instance.property
    start_date = instance.start_date.strftime("%Y-%m-%d")
    end_date = instance.end_date.strftime("%Y-%m-%d")
    if created:
        # This is a new Reservation object
        
        ReservationNotification.objects.create(
            user=instance.host, 
            reservation=instance, 
            content=f'A new reservation has been created for {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date}.',
            state='U',
        )
    else:
        # Check if the reservation has changed state
        if instance.previous_state != instance.state:
            if instance.state == 'Ap' and instance.previous_state == 'Pd':
                # Reservation has been approved
                ReservationNotification.objects.create(
                    user=instance.user, 
                    reservation=instance, 
                    content=f'Your reservation for {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date} has been approved.',
                    state='U',
                )
            elif instance.state == 'Cc':
                # Reservation has been cancelled
                ReservationNotification.objects.create(
                    user=instance.user,
                    reservation=instance, 
                    content=f'Your reservation for {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date} has been cancelled.',
                    state='U',
                )
            elif instance.state == 'Pc':
                # Reservation has been cancelled
                ReservationNotification.objects.create(
                    user=instance.host,
                    reservation=instance, 
                    content=f'Guest of {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date} has requested a cancellation.',
                    state='U',
                )
            