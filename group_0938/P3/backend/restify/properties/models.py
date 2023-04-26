from django.db import models
from django.utils.html import mark_safe
from user.models import User
from django.core.validators import RegexValidator
# Create your models here.
class Property(models.Model):
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    guests_cap = models.PositiveIntegerField(null=False, blank=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    beds = models.PositiveIntegerField(null = False, blank = False)
    baths = models.PositiveIntegerField(null = False, blank = False)
    unit_num = models.PositiveIntegerField(null = False, blank = False)
    street = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)

class Availability(models.Model):
    arrive_date = models.DateField()
    depart_date = models.DateField()
    total_price = models.PositiveIntegerField()
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)

class Amenity(models.Model):
    amenity = models.CharField(max_length=20)
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)

class Pictures(models.Model):
    picture = models.ImageField()
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    def img_preview(self): #new
        return mark_safe(f'<img src = "{self.picture.url}" width = "300"/>')



