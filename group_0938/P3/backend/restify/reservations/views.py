from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from datetime import datetime, timedelta
from .serializers import ReservationSerializer
from .models import Reservation
from properties.models import Availability, Property
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404

class AllReservationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        usertype = request.query_params.get('user_type')

        if usertype:
            if usertype == 'host':
                res = Reservation.objects.filter(host=user)
            elif usertype == 'guest':
                res = Reservation.objects.filter(user=user)
            else: 
                return Response(data={'error':"user_type can only be 'guest' or 'host'."},status=400)
        else:
            res = Reservation.objects.filter(Q(host=user) | Q(user=user))
        
        state = request.query_params.get('state')
        lst_states = ["Pd","Dn","Ex","Ap","Pc","Cc","Tm","Cm"]
        if state:
            if (not (state in lst_states)): 
                return Response(data={'error':"Invalid state."}, status=400)
            else:
                res = res.filter(state=state)

        order_by = request.query_params.get('order_by')
        order_by_lst = ["start_date", "end_date"]
        if order_by:
            if not order_by in order_by_lst:
                return Response(data={'error':"Invalid ordering."}, status=400)
            else:
                res = res.order_by(order_by)
        else:
            res = res.order_by('-id')

        page_number = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 2)
        paginator = Paginator(res, per_page)
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

        return Response(payload, status=200)
    
class Create(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        keys = ['property', 'start_date', 'end_date']
        if not all([key in data for key in keys]):
            return Response(data={'error':'missing keys'},status=400)
        
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
        
        if start_date >= end_date:
            return Response(data={'error':"start date must be earlier than end date"}, status = 400)       
        
        if not data['property'].isnumeric(): 
            return Response(data={'error':"Invalid property ID."}, status = 400)
        
        propty = get_object_or_404(Property, pk=data['property'])
        
        if request.user == propty.owner:
            return Response(data={'error':"You can't reserve on a property that you own."}, status = 400)

        avail = Availability.objects.filter(
            Q(prop=propty)&Q(arrive_date__gte=start_date)&Q(depart_date__lte=end_date))

        if not avail:
            return Response(data={'error':"The property is not available in the input time range."}, status = 400)  
        else:
            avail = avail.order_by('arrive_date')
            total_time = max(timedelta(), end_date - start_date)
            time = timedelta()
            for availability in avail:
                time += max(timedelta(), availability.depart_date - availability.arrive_date)
            
            time += timedelta(days=len(avail)-1)
            if time < total_time:
                return Response(data={'error':"The property is not consecutively available in the input time range."}, status = 400)  
            # previous_depart_date = None
            # consecutive_dates = True
            # for availability in avail:
                
            #     if previous_depart_date is not None:
            #         # Check if the previous depart date is the same as the current arrive date
            #         if previous_depart_date + timedelta(days=1) != availability.arrive_date:
            #             consecutive_dates = False
            #             return Response(data={'error':"The property is not consecutively available in the input time range."}, status = 400)  
            #     previous_depart_date = availability.depart_date
            
        for availability in avail:

            reserv = Reservation.objects.create(user=request.user, property = propty, host = propty.owner, 
                                            start_date = availability.arrive_date, end_date = availability.depart_date, price=availability.total_price)
        
        return Response({'status':200}, status=200)

        # if avail:
        #     avail = Availability.objects.get(prop=propty, arrive_date=start_date, depart_date=end_date,)
        #     reserv = Reservation.objects.create(user=request.user, property = propty, host = propty.owner, 
        #                                     start_date = start_date, end_date = end_date, price=avail.total_price)
        #     return Response({'status':200}, status=200)
        # else:
        #     return Response(data={'error':"The property is not available in the input time range."}, status = 400)      
    
class RequestCancel(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        data = request.data
        keys = ['id'] # reservation_id
        if not all([key in data for key in keys]):
            return Response(data={'error':'missing keys'},status=400)
        if not data['id'].isnumeric(): 
            return Response(data={'error':"Invalid property ID."}, status = 400)
        
        reserv = get_object_or_404(Reservation, pk=data['id'])
        if reserv.user != request.user:
            return Response(data={'error':'You can only cancel reservations made by you.'}, status=400)
        
        if reserv.state == 'Pc':
            return Response(data={'error':'A cancellation request is currently pending this reservation.'}, status=400)
        if reserv.state != 'Ap':
            return Response(data={'error':'Only approved reservations can be cancelled.'}, status=400)
        
        reserv.previous_state = reserv.state
        reserv.state = 'Pc'
        reserv.save()
        return Response({'status':200}, status=200)
    
class Terminate(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        data = request.data

        keys = ['id'] # reservation_id
        if not all([key in data for key in keys]):
            return Response(data={'error':'missing keys'},status=400)
        if not data['id'].isnumeric(): 
            return Response(data={'error':"Invalid property ID."}, status = 400)
        
        reserv = get_object_or_404(Reservation, pk=data['id'])
        if reserv.host != request.user:
            return Response(data={"error":"You can only terminate reservations that you're a host of."}, status=400)
        if reserv.state != 'Ap':
            return Response(data={'error':'Only approved reservations can be terminated.'}, status=400)
        
        reserv.previous_state = reserv.state
        reserv.state = 'Tm'
        reserv.save()

        # re-add availability
        avail = Availability.objects.create(arrive_date=reserv.start_date, depart_date=reserv.end_date, total_price=reserv.price, prop=reserv.property,)
        return Response({'status':200}, status=200)
    
class ApproveDenyPending(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        data = request.data

        keys = ['id', 'action'] # reservation_id

        if not all([key in data for key in keys]):
            return Response(data={'error':'missing keys'},status=400)
        if not data['id'].isnumeric(): 
            return Response(data={'error':"Invalid property ID."}, status = 400)
        
        reserv = get_object_or_404(Reservation, pk=data['id'])
        if reserv.host != request.user:
            return Response(data={"error':'You can only approve/deny reservations that you're a host of."}, status=400)
        if reserv.state != 'Pd':
            return Response(data={'error':'Only pending reservations can be approved/denied.'}, status=400)
        avail = Availability.objects.filter(prop=reserv.property).filter(arrive_date=reserv.start_date).filter(depart_date=reserv.end_date)
        
        reserv.previous_state = reserv.state
        if data['action'] == 'approve':
            if not avail:
                return Response(data={'error':'The property is currently not available at this time range.'}, status=400)
            # change state to approved, remove the availability from the property
            reserv.state = 'Ap'
            instance = Availability.objects.filter(prop=reserv.property).filter(arrive_date=reserv.start_date).filter(depart_date=reserv.end_date)
            instance.delete()
        elif data['action'] =='deny':
            reserv.state= 'Dn'
        else:
            return Response(data={'error':'Invalid action.'}, status=400)
        reserv.save()
        return Response({'status':200}, status=200)
    

class ApproveDenyCancel(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        data = request.data
        keys = ['id', 'action'] # reservation_id
        if not all([key in data for key in keys]):
            return Response(data={'error':'missing keys'},status=400)
        if not data['id'].isnumeric(): 
            return Response(data={'error':"Invalid property ID."}, status = 400)
        
        reserv = get_object_or_404(Reservation, pk=data['id'])
        if reserv.host != request.user:
            return Response(data={"error':'You can only approve/deny reservations that you're a host of."}, status=400)
        if reserv.state != 'Pc':
            return Response(data={'error':'Only reservations with pending cancellation can be approved/denied.'}, status=400)
        
        reserv.previous_state = reserv.state
        if data['action'] == 'approve':
            reserv.state = 'Cc'
            avail = Availability.objects.create(arrive_date=reserv.start_date, depart_date=reserv.end_date, total_price=reserv.price, prop=reserv.property,)
        elif data['action'] =='deny':
            reserv.state = 'Ap'
        else:
            return Response(data={'error':'Invalid action.'}, status=400)
        reserv.save()
        return Response({'status':200}, status=200)