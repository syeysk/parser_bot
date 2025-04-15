import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

CALLBACK_DATA_LOADFILE = 'load_file'


class HookBotView(APIView):
    def post(self, request):
        print(request.data)
        if request.META.get('HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN') != settings.TG_SECRET_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        message = request.data.get('message')
        if message and message['text'] == '/start':
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
            .post(f'{settings.TG_API_URL}/sendMessage', json=params)

        callback_query = request.data.get('callback_query')
        message = callback_query['message']
        if callback_query and callback_query['data'] == CALLBACK_DATA_LOADFILE:
            params = {
                'chat_id': message['chat']['id'],
                'text': 'Отправьте сообщение с прикреплённым excel-файлом',
            }
            requests.post(f'{settings.TG_API_URL}/sendMessage', json=params)

        return Response(status=status.HTTP_200_OK)
