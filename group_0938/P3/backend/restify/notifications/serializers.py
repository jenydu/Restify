from rest_framework import serializers
from .models import ReservationNotification
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationNotification
        fields = ['id', 'user', 'reservation', 'property','created_at', 'content', 'state']
        read_only_fields = ['id']