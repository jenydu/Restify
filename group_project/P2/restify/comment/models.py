from django.db import models
from reservations.models import Reservation
from django.conf import settings


class CommentOnProperty(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    )
    created_at = models.DateField(auto_now_add=True)


class HostReply(models.Model):
    comment = models.OneToOneField(CommentOnProperty, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class CommentOnReply(models.Model):
    reply = models.OneToOneField(HostReply, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class CommentOnUser(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviewer"
    )
    content = models.TextField()
    rating = models.IntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    )
    created_at = models.DateField(auto_now_add=True)
