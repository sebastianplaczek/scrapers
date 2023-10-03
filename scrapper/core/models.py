from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class LinksToScrap(models.Model):
    link = models.CharField(max_length=100,null=False)
    item_name = models.CharField(max_length=50,blank=True,null=True)
    create_date = models.DateTimeField(default=timezone.now)
    service = models.CharField(max_length=20,null=False)
    active = models.BooleanField(default=True)
    deactivate_date = models.DateTimeField(blank=True,null=True)

class UsersLinks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    linktoscrap = models.ForeignKey(LinksToScrap, on_delete=models.CASCADE)
    conditional = models.CharField(max_length=10,blank=True,null=True)
    conditional_price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=timezone.now)

class DailyScraps(models.Model):
    linktoscrap = models.ForeignKey(LinksToScrap, on_delete=models.CASCADE)
    price = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=10)
    discount_price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    create_date = models.DateTimeField(default=timezone.now)

class ServicesLogs(models.Model):
    linktoscrap = models.ForeignKey(LinksToScrap, on_delete=models.CASCADE)
    error = models.CharField(max_length=20,null=False)
    service = models.CharField(max_length=20,null=False)
    content = models.CharField(max_length=1000,blank=True,null=True)
    create_date = models.DateTimeField(default=timezone.now)

class ServicesErrors(models.Model):
    service_name = models.CharField(max_length=30,null=False)
    error = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)


class Otodom(models.Model):
    type = models.CharField(max_length=10)
    link = models.CharField(max_length=255,blank=True,null=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    address_params = models.CharField(max_length=1000,blank=True,null=True)
    price = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=10)
    price_per_m = models.IntegerField(blank=True,null=True)
    rooms = models.IntegerField(blank=True,null=True)
    size = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=10)
    active = models.BooleanField(default=True)
    additional_params_1 = models.CharField(max_length=1000)
    additional_params_2 = models.CharField(max_length=1000)
    vivodeship = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    seller = models.CharField(max_length=255,blank=True,null=True)
    filled = models.IntegerField(default=0)
    page = models.IntegerField(blank=True,null=True)
    bumped = models.IntegerField(default=0,blank=True,null=True)
    new = models.IntegerField(default=0,blank=True,null=True)

class Otodom_fills(models.Model):
    link = models.CharField(max_length=255, blank=True, null=True)
    additional_params_1 = models.CharField(max_length=1000)
    additional_params_2 = models.CharField(max_length=1000)
    address_params = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    vivodeship = models.CharField(max_length=50, blank=True, null=True)


class OtodomLogs(models.Model):
    link = models.CharField(max_length=255,blank=True,null=True)
    error = models.CharField(max_length=10000,null=False)
    type = models.CharField(max_length=10)
    create_date = models.DateTimeField(default=timezone.now)
    robot = models.CharField(max_length=25)

class Workers(models.Model):
    type = models.CharField(max_length=10)
    number =  models.IntegerField(blank=True,null=True)
    active = models.BooleanField(default=True)