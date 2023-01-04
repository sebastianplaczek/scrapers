
from django.core.management.base import BaseCommand
from core.views.test_view import MemoryCheck

password = 'ZdzislawOgurekMM1'
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        o = MemoryCheck()
        o.run()

