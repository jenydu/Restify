from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Property, Amenity, Pictures, Availability, Amenity, Pictures
from collections.abc import Iterable  
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core import serializers
from django.http import JsonResponse
from django.core import serializers
from rest_framework.renderers import JSONRenderer
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

# Create your views here.
AMENITIES = set(['Fireplace', 'Sauna', 'Tub', 'Kitchen', 'Tv', 'Sofa'])
class Create(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        data = request.data

        keys = ['city', 'province', 'country', 'guests_cap', 'images', 'amenities', 'beds', 'baths','unit_num', 'street', 'desc']

        if not all([key in data for key in keys]):
            return Response(data={'error':'missing keys'},status=400)

        if not all([key in AMENITIES for key in data.getlist('amenities')]):
            return Response(data={'error':'invalid amenities'},status=400)

        if not data.get('city').isalpha() or not data.get('country').isalpha() or not data.get('country').isalpha():
            return Response(data={'error':'location data must be alpha characters'},status=400)

        try:
            prop = Property.objects.create(owner=request.user, city=data['city'], province=data['province'], country=data['country'], guests_cap=data['guests_cap'], beds=data.get('beds'), baths=data.get('baths'), desc=data.get('desc'), unit_num=data.get('unit_num'), street=data.get('street'))
        except:
            return Response(data={'error':'Could not insert'}, status=400)

        for amenity in data.getlist('amenities'):
            try:
                Amenity.objects.create(amenity=amenity, prop=prop)
            except:
                return Response(data={'error':'Could not insert amenity'}, status=400)

        for image in data.getlist('images'):
            try:
                Pictures.objects.create(picture=image, prop = prop)
            except:
                return Response(data={'error':'Could not insert images'}, status=400)
        return Response({'status':200}, status=200)

class Update(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            prop = Property.objects.get(id=pk)
        except Property.DoesNotExist:
            return Response(data={'msg: Property not found'}, status=404)

        if request.user != prop.owner:
            return Response(data={'msg: You are not allowed to edit this proeprty'},status=403)
        
        availability_keys = ['arrive_date', 'depart_date', 'price' ]
        data = request.data

        if not all([key in data for key in availability_keys]) and not 'amenities' in data and not 'guests_cap' in data and not 'beds' in data and not 'baths' in data and not 'images' in data:
            return Response(data={'msg:Invalid request'} ,status=400)


        
        if 'arrive_date' in data:
            price = data.get('price')
            try:
                start_date = datetime.strptime(data.get('arrive_date'), '%Y/%m/%d')
                end_date = datetime.strptime(data.get('depart_date'),'%Y/%m/%d')
            except:
                return Response(data={'error':'Could not parse dates'}, status=400)

            if Availability.objects.filter(arrive_date__range=[start_date,end_date]).filter(prop=prop).first() != None or \
                Availability.objects.filter(depart_date__range=[start_date,end_date]).filter(prop=prop).first() != None:
                return Response(data={'msg':'Date range overlaps with pre existing availability'}, status=400)

            if start_date >= end_date:
                return Response(data={'msg':'Start date must be less than depart date'}, status=400)
            
            try:
                Availability.objects.create(prop=prop, total_price=price, arrive_date=start_date, depart_date=end_date)
            except:
                return Response(data={'error':'Could not insert availability'}, status=400)
        
        if 'amenities' in data:
            if not all([key in AMENITIES for key in data.getlist('amenities')]):
                return Response(data={'error':'invalid amenities'},status=400)
            Amenity.objects.filter(prop=prop).delete()
            for amenity in data.getlist('amenities'):
                try:
                    Amenity.objects.create(prop=prop, amenity=amenity)
                except:
                    return Response(data={'error':'Could not update amenity'}, status=400)

        if 'guests_cap' in data:
            try:
                prop.guests_cap = data.get('guests_cap')
                prop.save()
            except:
                return Response(data={'error':'Could not update guests_cap'}, status=400)
        
        if 'beds' in data:
            try:
                prop.beds = data.get('beds')
                prop.save()
            except:
                return Response(data={'error':'Could not update beds'}, status=400)   

        if 'baths' in data:
            try:
                prop.baths = data.get('baths')
                prop.save()
            except:
                return Response(data={'error':'Could not update baths'}, status=400)      

        if 'images' in data:
            Pictures.objects.filter(prop=prop).delete()
            for image in data.getlist('images'):
                try:
                    Pictures.objects.create(picture=image, prop = prop)
                except:
                    return Response(data={'error':'Could not insert images'}, status=400)

        
        return Response(status=200)

class Search(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        data = request.data
        location_keys = ['city', 'province', 'country']
        available_dates_keys = ['arrive_date', 'depart_date']
        price_order_keys = ['arrive_date', 'depart_date', 'price']
        guests_cap = data.get('guests_cap')
        order_by = data.get('order_by')
        beds = data.get('beds')
        baths = data.get('baths')
        availability = None

        props = Property.objects.all()

        if all(key in data for key in location_keys):
            city = data.get('city')
            province = data.get('province')
            country = data.get('country')
            try:
                props = props.filter(city=city, province=province, country=country)
            except:
                return Response(data={'error':'Could not filter on location'}, status=400)
        if all(key in data for key in available_dates_keys):
            try:
                start_date = datetime.strptime(data.get('arrive_date'), '%Y/%m/%d')
                end_date = datetime.strptime(data.get('depart_date'),'%Y/%m/%d')
            except:
                return Response(data={'error':'Could not parse dates'}, status=400)

            try:     
                availability = Availability.objects.filter(arrive_date__gte=start_date).filter(depart_date__lte=end_date).values('prop_id')
            except:
                return Response(data={'error':'Could not filter on availability'}, status=400)

            props = props.filter(id__in=availability)


        if guests_cap:
            try:
                props = props.filter(guests_cap=guests_cap)
            except:
                return Response(data={'error':'Could not filter on guests cap'}, status=400)

        if beds:
            try:
                props = props.filter(beds=beds)
            except:
                return Response(data={'error':'Could not filter on beds'}, status=400)
        
        if baths:
            try:
                props = props.filter(baths=baths)
            except:
                return Response(data={'error':'Could not filter on baths'}, status=400)
        
        
        if order_by == 'baths':
            props = props.order_by('baths')
        
        if order_by == 'beds':
            props=props.order_by('beds')

        page_number = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 1)

        paginator = Paginator(props, per_page)
        page_obj = paginator.get_page(page_number)

        # data = [{'id':kw.id} for kw in page_obj.object_list]

        data = []
        for obj in page_obj.object_list:
            payload_obj = {}
            payload_obj['id'] = obj.id
            payload_obj['city'] = obj.city
            payload_obj['country'] = obj.country
            payload_obj['desc'] = obj.desc
            payload_obj['province'] = obj.province
            payload_obj['beds'] = obj.beds
            payload_obj['baths'] = obj.baths
            payload_obj['guests_cap'] = obj.guests_cap
            image = Pictures.objects.filter(prop=obj).first().picture.name
            payload_obj['picture'] = image
            payload_obj['street'] = obj.street
            payload_obj['unit_num'] = obj.unit_num
            if availability == None:
                earliest_start = Availability.objects.filter(prop=obj).order_by('arrive_date').first()
                payload_obj['arrive_date'] = earliest_start.arrive_date
                payload_obj['depart_date'] = earliest_start.depart_date
                payload_obj['price'] = earliest_start.total_price

            
            data.append(payload_obj)

        payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },

        "data": data
        }

        return JsonResponse(payload, status=200)

class Delete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request, pk):
        try:
            prop = Property.objects.get(id=pk)
        except Property.DoesNotExist:
            return Response(data={'msg: Property not found'}, status=404)

        if request.user != prop.owner:
            return Response(data={'msg: You are not allowed to edit this proeprty'},status=403)

        prop.delete()
        return Response(data={'msg:deleted'}, status=200)    

class DeleteAvailability(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,pk):
        data = request.data
        try:
            prop = Property.objects.get(id=pk)
        except Property.DoesNotExist:
            return Response(data={'msg: Property not found'}, status=404)

        if request.user != prop.owner:
            return Response(data={'msg: You are not allowed to edit this proeprty'},status=403)

        try:
            start_date = datetime.strptime(data.get('arrive_date'), '%Y/%m/%d')
            end_date = datetime.strptime(data.get('depart_date'),'%Y/%m/%d')

        except:
            return Response(data={'error':'Could not parse dates'}, status=400)

        if start_date >= end_date:
            return Response(data={'msg':'Start date must be less than depart date'}, status=400)

        try:
            Availability.objects.filter(arrive_date__lte=end_date).filter(depart_date__gte=start_date).delete()
        except:
            return Response(data={'error':'Could not delete availability'}, status=400)

        return Response({'msg: deleted'},status=200)


def get_propty(request, prop_id):
    prop = get_object_or_404(Property, pk=prop_id)
    response = {
        'city': prop.city,
        'province': prop.province,
        'country': prop.country,
        'street': prop.street,
        'unit_num': prop.unit_num,

    }
    return JsonResponse(response)