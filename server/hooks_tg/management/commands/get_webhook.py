import requests
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Получает и отображает установленный хук'

    def handle(self, *args, **options):
        response = requests.post(f'{settings.TG_API_URL}/getWebhookInfo')
        if response.status_code == 200:
            response_json = response.json()
            if response_json['ok']:
                result = response_json['result']
                url = result.pop('url', '')
                self.stdout.write(f'Установленный URL: {url}\nПодробно:\n')
                self.stdout.write(str(result))
                return

        self.stdout.write(f'Ошибка получения хука: {response.content}\n\n')
