
from django.core.management.base import BaseCommand
from core.views.memory_check_view import MemoryCheck

#password = 'ZdzislawOgurekMM1'
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        o = MemoryCheck()
        o.run()

