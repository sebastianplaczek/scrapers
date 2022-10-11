from django.core.management.base import BaseCommand
from django.utils import timezone
import time

from core.views.mohito_view import MohitoScrapRobot
from core.models import MohitoToScrap,MohitoDailyScraps

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        endpoint_list = MohitoToScrap.objects.filter(active=True).all()

        scraper = MohitoScrapRobot()
        scraper.inactive_site_error_check()

        if scraper.correct_structure:
            for object in endpoint_list:
                scraper.run(endpoint=object.endpoint)
                time.sleep(3)
