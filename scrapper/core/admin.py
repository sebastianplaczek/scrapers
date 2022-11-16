from django.contrib import admin

# Register your models here.

from .models import LinksToScrap,DailyScraps

admin.site.register(LinksToScrap)
admin.site.register(DailyScraps)
