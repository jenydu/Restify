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
        notif = ReservationNotification.objects.filter(user=user).order_by('-created_at')

        state = request.query_params.get('state')
        lst_states = ["U","R"]
        if state:
            if (not (state in lst_states)): 
                return Response(data={'error':"Invalid state."}, status=400)
            else:
                notif = notif.filter(state=state)
        
        page_number = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 4)
        paginator = Paginator(notif, per_page)
        page_obj = paginator.get_page(page_number)

        serializer = ReservationSerializer(page_obj, many=True)



        payload = {
            "page": {
                "current": page_obj.number,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            },
            "data": serializer.data
        }

        # for notif in page_obj:
        #     notif.state = 'R' # change to read
        #     notif.save()
        return Response(payload, status=200)
    
class NotificationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        try:
            notification = ReservationNotification.objects.get(id=notification_id, user=request.user)
        except ReservationNotification.DoesNotExist:
            return Response(data={'error':"Notification not found."}, status=404)
        if notification.state =='U':
            notification.state = 'R'
        elif notification.state == 'R':
            notification.state = 'U'
        
        notification.save()

        serializer = ReservationSerializer(notification)
        return Response(serializer.data, status=200)
    
class NotificationDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReservationNotification.objects.all()

    def delete(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset().filter(user=user).filter(state='R')
        deleted_count, _ = queryset.delete()
        return Response({"deleted_count": deleted_count}, status=204)