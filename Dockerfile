FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
VOLUME /app /static
WORKDIR /app

COPY . .

RUN apt-get update && apt-get -y install git && python3 -m pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt