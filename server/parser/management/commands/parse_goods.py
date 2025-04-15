import math
import re

import lxml.html as html
import requests
from django.core.management.base import BaseCommand
from parser.models import GoodRule


class Command(BaseCommand):
    help = 'Парсит товары по правилам, сохранённым в БД'

    def handle(self, *args, **options):
        price_re = re.compile(r'\d+')
        prices_sum = 0
        count_goods = 0
        for count_goods, good_rule in enumerate(GoodRule.objects.all()):
            response = requests.get(good_rule.url)
            if response.status_code == 200:
                response_text = response.text
                document = html.document_fromstring(response_text)
                price_elements = document.xpath(good_rule.xpath)
                if price_elements:
                    raw_price = price_elements[0].text_content()
                    price = int(price_re.findall(raw_price.strip())[0])
                    title = good_rule.title
                    prices_sum += price
                    self.stdout.write(f'{title}: {price}')

        self.stdout.write('')
        average_price = (prices_sum / count_goods) if count_goods > 0 else 0 
        self.stdout.write(f'Средняя цена: {average_price}')