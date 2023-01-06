
from django.core.management.base import BaseCommand
from core.views.notify import Notify

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # receiver_email = "p.kidawa@onnetwork.pl"

        o = Notify()
        o.send_email()

