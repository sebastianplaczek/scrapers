from django.core.management.base import BaseCommand
from core.views.zalando_view import ZalandoScrapRobot
from django.utils import timezone
import time

from core.models import ZalandoToScrap,ZalandoDailyScraps

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        zalando_list = ZalandoToScrap.objects.filter(active=True).all()

        scraper = ZalandoScrapRobot()
        for object in zalando_list:
            scraper.run(endpoint=object.endpoint)
            time.sleep(3)
