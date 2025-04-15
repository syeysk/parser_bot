from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class HookBotView(APIView):
    def post(self, request):
        print(request.data)
        if request.META.get('HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN') != settings.TG_SECRET_TOKEN:
            print('forbidden')
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_200_OK)
