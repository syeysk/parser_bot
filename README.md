Что не реализовано:
- верификация хука (действительно ли запрос пришёл от телеграма)

# Установка на Linux

Скачайте репозиторий:

```sh
git clone https://github.com/syeysk/parser_bot && cd parser_bot
```

Заполните переменные окружения, добавив и заполнив файл `.env`:
```sh
cd server
cp example_env .env
cd ..
```

Соберите образ и запустите контейнер:

```sh
docker-compose -f docker-compose.yml up -d --build
```

## Проверка доступности сервера

<http://127.0.0.1:8020/admin>

## Настройте Nginx + Debian для глобального доступа

Ниже вместо домена `bot.syeysk.ru` подставьте свой.

Создайте файл `/etc/nginx/conf.d/bot.syeysk.ru.conf` и запишите в него настройки для Nginx:

```
server {
    listen 80;
    listen [::]:80;
    server_name bot.syeysk.ru www.bot.syeysk.ru;
    root /usr/share/nginx/html/bot.syeysk.ru;
    location / {
        proxy_pass http://127.0.0.1:8020;
    }
    location /static/ {
        sendfile on;
        root /usr/share/nginx/html/parser_bot;
    }
    location /media/ {
        sendfile on;
        root /usr/share/nginx/html/parser_bot;
    }
    location = /favicon.ico {
       sendfile on;
       root /usr/share/nginx/html/parser_bot/static;
    }
}
```

Если нужно установить сертификат SSL для домена, то [следуйте инструкциям](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/) - поправка: возможно, на Вашем сервере нужно вместо команды `python` использовать `python3`.
Если Вы ранее выполняли команды из этой инструкции для других серверов Платформы, то достаточно выполнить команду `sudo certbot --nginx -d bot.syeysk.ru -d www.bot.syeysk.ru`, чтобы получить сертификат.
