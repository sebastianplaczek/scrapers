from django.core.management.base import BaseCommand
from core.views.otodom_scrapper_view import OtodomScrapper

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        o = OtodomScrapper()
        o.test()
