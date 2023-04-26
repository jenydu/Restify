from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'host', 'property', 'start_date', 'end_date', 'state', 'previous_state']
        read_only_fields = ['id']