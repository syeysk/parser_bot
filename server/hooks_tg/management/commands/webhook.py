import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import resolve_url


class Command(BaseCommand):
    help = 'Устанавливает хук для получения обновлений из Телеграма'

    def add_arguments(self, parser):
        url_path = resolve_url('hook_tg')
        parser.add_argument(
            '--url',
            help='URL, на который Телеграм будет отправлять обновления',
            default=f'{settings.SITE_URL}{url_path}'
        )

    def handle(self, *args, **options):
        response = requests.post(
            f'{settings.TG_API_URL}/setWebhook',
            json={'url': options['url'], 'secret_token': settings.TG_SECRET_TOKEN},
        )
        if response.status_code == 200:
            response_json = response.json()
            if response_json['ok']:
                self.stdout.write('Хук успешно установлен')

        self.stdout.write(f'Ошибка установки хука: {response.content}\n\n')
