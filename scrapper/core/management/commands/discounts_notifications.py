
from django.core.management.base import BaseCommand
from core.views.discounts_notifications import Notify

#password = 'ZdzislawOgurekMM1'
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        o = Notify()
        o.run()

