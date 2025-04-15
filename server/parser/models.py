from django.db import models


class GoodRule(models.Model):
    title = models.CharField('Название', max_length=240)
    url = models.CharField('URL страницы товара', max_length=240)
    xpath = models.CharField('Путь к элементу с ценой', max_length=240)

    class Meta:
        verbose_name = 'Правило парсинга товара'
        verbose_name_plural = 'Правила парсинга товара'
