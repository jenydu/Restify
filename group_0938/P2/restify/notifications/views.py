from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters

from .serializers import ReservationSerializer
from .models import Reservation, ReservationNotification
from django.core.paginator import Paginator
from django.db.models import Q

class AllNotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        notif = ReservationNotification.objects.filter(user=user)

        state = request.query_params.get('state')
        lst_states = ["U","R"]
        if state:
            if (not (state in lst_states)): 
                return Response(data={'error':"Invalid state."}, status=400)
            else:
                notif = notif.filter(state=state)
        
        page_number = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 1)
        paginator = Paginator(notif, per_page)
        page_obj = paginator.get_page(page_number)

        serializer = ReservationSerializer(page_obj, many=True)
        res = serializer.data
        for notif in page_obj:
            notif.state = 'R' # change to read
            notif.save()
        return Response(res, status=200)
    
class NotificationDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReservationNotification.objects.all()

    def delete(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset().filter(user=user).filter(state='R')
        deleted_count, _ = queryset.delete()
        return Response({"deleted_count": deleted_count}, status=204)