# Бот + парсер товаров

Приложение представляет собой:
- Телеграм-бот, позволяющий добавить правила для парсинга товаров.
- Простой парсер по правилам, добавленных через бота.

Сделано в рамках тестового задания.

## Что не реализовано

- удаление обработанного excel-файла
- при добавлении строк из файла в базу - проверка на уникальность
- обработка ошибок
- валидация файла на корректность формата перед открытием
- валидация струткуры файла
- блокировка запросов, исходящих не от телеграма

## Особенности

- Бот реализован как веб-хуки, без внешней библиотеки. Если делать с библиотекой и без хука (long pulling), то необходимость в настройке веб-сервера отпадёт.
- Подразумевается, что цена товара состоит только из целой части (справа и слева от цены могут быть любые символы)

## Установка на Linux

Скачайте репозиторий:

```sh
git clone https://github.com/syeysk/parser_bot && cd parser_bot/server
```

Заполните переменные окружения, добавив и заполнив файл `.env`:
```sh
cp example_env .env
cd ..
```

Соберите образ и запустите контейнер:

```sh
docker-compose -f docker-compose.yml up -d --build
```

### Проверка доступности сервера

<http://127.0.0.1:8020/admin>

### Настройте Nginx + Debian для глобального доступа

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
Если Вы ранее выполняли команды из этой инструкции для других серверов, то достаточно выполнить команду `sudo certbot --nginx -d bot.syeysk.ru -d www.bot.syeysk.ru`, чтобы получить сертификат.

## Команды для администрирования

Запуск парсера:
```sh
python manage.py parse_goods
```

Установка хука для телеграма:
```sh
python manage.py webhook
```

Просмотр установленного хука:
```sh
python manage.py get_webhook
```
