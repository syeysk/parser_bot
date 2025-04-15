import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from parser.models import GoodRule


class Command(BaseCommand):
    help = 'Парсит товары по правилам, сохранённым в БД'

    def handle(self, *args, **options):
        for good_rule in GoodRule.objects.all():
            response = requests.get(good_rule['url'])
            if response.status_code == 200:
                response_text = response.text
                price = 0
                title = good_rule['title']
                self.stdout.write(f'{title}: {price}')
