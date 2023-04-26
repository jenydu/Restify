from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Bank(models.Model):
    name = models.CharField(max_length=200, null=False)
    swift_code = models.CharField(max_length=200, null=False)
    inst_num = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Branch(models.Model):
    name = models.CharField(max_length=200, null=False)
    transit_num = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    email = models.EmailField(default='admin@utoronto.ca')
    capacity = models.PositiveIntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
