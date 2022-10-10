from django.core.management.base import BaseCommand
from core.views.reserved_view import ReservedScrapRobot
from django.utils import timezone
import time

from core.models import ReservedToScrap,ReservedDailyScraps

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        endpoint_list = ReservedToScrap.objects.filter(active=True).all()

        scraper = ReservedScrapRobot()
        for object in endpoint_list:
            scraper.run(endpoint=object.endpoint)
            time.sleep(3)
