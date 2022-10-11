from django.contrib import admin

# Register your models here.

from .models import ZalandoToScrap,\
                    ZalandoDailyScraps,\
                    ReservedToScrap,\
                    ReservedDailyScraps,\
                    MohitoToScrap, \
                    MohitoDailyScraps

admin.site.register(ZalandoDailyScraps)
admin.site.register(ZalandoToScrap)

admin.site.register(ReservedDailyScraps)
admin.site.register(ReservedToScrap)

admin.site.register(MohitoDailyScraps)
admin.site.register(MohitoToScrap)