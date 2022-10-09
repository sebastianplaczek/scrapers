from django.core.management.base import BaseCommand
from core.views.zalando_view import Zalando

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        test_endpoints = [
            'https://www.zalando.pl/selfieroom-sukienka-letnia-black-sjx21c01s-q11.html',
            'https://www.zalando.pl/adidas-originals-ozrah-unisex-sneakersy-niskie-black-ad115o1bm-q11.html',
            'https://www.zalando.pl/nike-performance-legginsy-dynamic-berryiron-gre-n1241e1hk-i12.html',
            'https://www.zalando.pl/nike-sportswear-wmns-air-max-97-nn-sneakersy-niskie-whitelight-sail-ni111a164-a11.html',
            'https://www.zalando.pl/huf-swirl-oversized-bluza-rozpinana-olive-h0h21j00l-t11.html',
            'https://www.zalando.pl/pullandbear-loose-fit-parachute-spodnie-materialowe-mottled-black-puc21a0pk-q11.html',
            'https://www.zalando.pl/nike-sportswear-air-max-97-tenisowki-i-trampki-ni112o00k-a11.html'
        ]

        model = Zalando()
        for url in test_endpoints:
            model.run(url)