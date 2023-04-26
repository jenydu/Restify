from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import ReservationNotification
from reservations.models import Reservation
from properties.models import Property
from comment.models import CommentOnProperty
from datetime import datetime, timedelta


@receiver(post_save, sender=CommentOnProperty)
def create_proptycomment_notification(sender, instance, created, **kwargs):
    res = instance.reservation
    propty = res.property
    if created:
        # new comment
        ReservationNotification.objects.create(
            user=propty.owner,
            property=propty,
            reservation=res, 
            content=f'A new comment has been posted on {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country} (Property ID: {propty.id}).',
            state='U',
        )

@receiver(post_save, sender=Reservation)
def create_reservation_notification(sender, instance, created, **kwargs):
    propty = instance.property
    start_date = instance.start_date.strftime("%Y-%m-%d")
    end_date = instance.end_date.strftime("%Y-%m-%d")
    if created:
        # new reservation
        ReservationNotification.objects.create(
            user=instance.host, 
            reservation=instance, 
            property = propty,
            content=f'A new reservation has been created for {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date}.',
            state='U',
        )
    else:
        # Check if the reservation has changed state
        if instance.previous_state != instance.state:
            if instance.state == 'Ap' and instance.previous_state == 'Pd':
                # Pending approved
                ReservationNotification.objects.create(
                    user=instance.user, 
                    reservation=instance, 
                    property = propty,
                    content=f'Your reservation request for {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date}, has been approved.',
                    state='U',
                )
            elif instance.state == 'Dn':
                # Pending denied
                ReservationNotification.objects.create(
                    user=instance.user,
                    reservation=instance, 
                    property = propty,
                    content=f'Your reservation request for {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date}, has been denied.',
                    state='U',
                )
            elif instance.state == 'Cc':
                # cancel request approved
                ReservationNotification.objects.create(
                    user=instance.user,
                    reservation=instance, 
                    property = propty,
                    content=f'Your cancellation request for reservation on {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date}, has been approved.',
                    state='U',
                )
            elif instance.state == 'Ap' and instance.previous_state == 'Pc':
                # cancel request denied
                ReservationNotification.objects.create(
                    user=instance.user,
                    reservation=instance, 
                    property = propty,
                    content=f'Your cancellation request for reservation on {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date}, has been denied.',
                    state='U',
                )
            elif instance.state == 'Pc':
                # receive cancellation request (host)
                ReservationNotification.objects.create(
                    user=instance.host,
                    reservation=instance, 
                    property = propty,
                    content=f'Guest of {propty.unit_num} {propty.street}, {propty.city}, {propty.province}, {propty.country}, from {start_date} to {end_date}, has requested a cancellation.',
                    state='U',
                )
            