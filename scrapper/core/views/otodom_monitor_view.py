

from core.models import OtodomMonitor,Otodom

class OtodomMonit():

    def run(self):
        self.unfilled = len(Otodom.objects.filter(filled=0))
        OtodomMonitor.objects.create(describe='10 workers; normal filler',indicator=self.unfilled)
        print('Done')




