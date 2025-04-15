import uuid

import pandas
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from parser.models import GoodRule

CALLBACK_DATA_LOADFILE = 'load_file'


def process_file(file_path):
    goods = pandas.read_excel(file_path)
    added_titles = []
    for good in goods.itertuples():
        title = good.title
        good_rule = GoodRule(title=title, url=good.url, xpath=good.xpath)
        good_rule.save()
        added_titles.append(title)
    
    return added_titles


class HookBotView(APIView):
    def post(self, request):
        print(request.data)
        if request.META.get('HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN') != settings.TG_SECRET_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        message = request.data.get('message')
        if message:
            text = message.get('text')
            if text == '/start':
                button = {
                    'text': 'Загрузить файл',
                    'callback_data': CALLBACK_DATA_LOADFILE,
                }
                params = {
                    'chat_id': message['chat']['id'],
                    'text': 'Пожалуйста, выберите действие:',
                    'reply_markup': {
                        'inline_keyboard': [[button]],
                    },
                }
                requests.post(f'{settings.TG_API_URL}/sendMessage', json=params)
            
            document = message.get('document')
            if document:
                params = {'file_id': document['file_id']}
                response = requests.post(f'{settings.TG_API_URL}/getFile', json=params)
                response_json = response.json()
                print(response_json)
                file_object = response_json['result']
                file_path = file_object['file_path']
                file_url = f'https://api.telegram.org/file/bot{settings.TG_TOKEN}/{file_path}'
                response = requests.get(file_url)
                
                file_base_name = uuid.uuid4().hex
                file_local_path = file_base_name
                with open(file_local_path, 'wb') as file_local:
                    file_local.write(response.content)
                
                added_titles = process_file(file_local_path)
                added_titles_str = ', '.join(added_titles)
                params = {
                    'chat_id': message['chat']['id'],
                    'text': f'Следующие товары добавлены для парсинга:\n{added_titles_str}',
                }
                requests.post(f'{settings.TG_API_URL}/sendMessage', json=params)

        callback_query = request.data.get('callback_query')
        if callback_query and callback_query['data'] == CALLBACK_DATA_LOADFILE:
            message = callback_query['message']
            params = {
                'chat_id': message['chat']['id'],
                'text': 'Отправьте сообщение с прикреплённым excel-файлом',
            }
            requests.post(f'{settings.TG_API_URL}/sendMessage', json=params)

        return Response(status=status.HTTP_200_OK)
