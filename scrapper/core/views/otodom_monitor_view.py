

from core.models import OtodomMonitor,Otodom

class OtodomMonit():

    def run(self):
        self.unfilled = len(Otodom.objects.filter(filled=0))
        if self.unfilled>0:
            OtodomMonitor.objects.create(describe='8 workers; normal filler',indicator=self.unfilled)
        print('Done')




