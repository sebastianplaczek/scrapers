from django.contrib import admin

# Register your models here.

from .models import ZalandoToScrap,ZalandoDailyScraps

admin.site.register(ZalandoDailyScraps)
admin.site.register(ZalandoToScrap)