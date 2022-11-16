from django.core.management.base import BaseCommand
from core.views.reserved_view import ReservedScrapRobot
from django.utils import timezone
import time

from core.models import LinksToScrap

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        links_list = LinksToScrap.objects.filter(active=True,service='reserved').all()

        scraper = ReservedScrapRobot()
        scraper.inactive_site_error_check()
        if scraper.correct_structure:
            for object in links_list:
                scraper.run(link=object.link)
                time.sleep(3)
