from django.contrib import admin

# Register your models here.

from .models import ZalandoToScrap,ZalandoDailyScraps,ReservedToScrap,ReservedDailyScraps

admin.site.register(ZalandoDailyScraps)
admin.site.register(ZalandoToScrap)
admin.site.register(ReservedDailyScraps)
admin.site.register(ReservedToScrap)