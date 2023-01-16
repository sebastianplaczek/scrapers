from django.core.management.base import BaseCommand
from core.views.otodom_params_filler import OtodomFiller

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        o = OtodomFiller()
        o.run()
        #o.test()
