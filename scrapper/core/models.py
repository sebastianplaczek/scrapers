from django.db import models
from django.utils import timezone



class ZalandoToScrap(models.Model):
    endpoint = models.CharField(max_length=100,null=False)
    create_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    deactivate_date = models.DateTimeField(blank=True,null=True)

class ZalandoDailyScraps(models.Model):
    zalandotoscrap = models.ForeignKey(ZalandoToScrap, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=10)

class ZalandoLogs(models.Model):
    zalandotoscrap = models.ForeignKey(ZalandoToScrap, on_delete=models.CASCADE)
    error = models.CharField(max_length=20,null=False)
    content = models.CharField(max_length=1000,blank=True,null=True)
    create_date = models.DateTimeField(default=timezone.now)

class ServicesErrors(models.Model):
    service_name = models.CharField(max_length=30,null=False)
    error = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)


class ReservedToScrap(models.Model):
    endpoint = models.CharField(max_length=100,null=False)
    create_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    deactivate_date = models.DateTimeField(blank=True,null=True)

class ReservedDailyScraps(models.Model):
    toscrap = models.ForeignKey(ReservedToScrap, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    discount_price = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=10)
    price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
class ReservedLogs(models.Model):
    toscrap = models.ForeignKey(ReservedToScrap, on_delete=models.CASCADE)
    error = models.CharField(max_length=20,null=False)
    content = models.CharField(max_length=1000,blank=True,null=True)
    create_date = models.DateTimeField(default=timezone.now)

class MohitoToScrap(models.Model):
    endpoint = models.CharField(max_length=100,null=False)
    create_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    deactivate_date = models.DateTimeField(blank=True,null=True)

class MohitoDailyScraps(models.Model):
    toscrap = models.ForeignKey(MohitoToScrap, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    discount_price = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=10)
    price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
class MohitoLogs(models.Model):
    toscrap = models.ForeignKey(MohitoToScrap, on_delete=models.CASCADE)
    error = models.CharField(max_length=20,null=False)
    content = models.CharField(max_length=1000,blank=True,null=True)
    create_date = models.DateTimeField(default=timezone.now)