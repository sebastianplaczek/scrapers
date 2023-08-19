from django.core.management.base import BaseCommand
from core.views.discord_midjourney_view1 import Midjourney

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        o = Midjourney()
        o.run()
        #o.test()
