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
