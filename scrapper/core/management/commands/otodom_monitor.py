from django.core.management.base import BaseCommand
from core.views.otodom_monitor_view import OtodomMonit

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        o = OtodomMonit()
        o.run()
        #o.test()
