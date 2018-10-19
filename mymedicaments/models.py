from django.contrib.auth import get_user_model
from django.db import models


class Medicament(models.Model):
    CATEGORY_EMPTY_KEY = 0
    CATEGORY_EMPTY_VALUE = 'Пусто'
    CATEGORY_NOSE_KEY = 1
    CATEGORY_NOSE_VALUE = 'Для носа'
    CATEGORY_THROAT_KEY = 2
    CATEGORY_THROAT_VALUE = 'Для горла'
    CATEGORY_VITAMINE_KEY = 3
    CATEGORY_VITAMINE_VALUE = 'Витамины'
    CATEGORY_BAA_KEY = 4
    CATEGORY_BAA_VALUE = 'БАДы'

    CATEGORIES = (
        (CATEGORY_EMPTY_KEY, CATEGORY_EMPTY_VALUE),
        (CATEGORY_NOSE_KEY, CATEGORY_NOSE_VALUE),
        (CATEGORY_THROAT_KEY, CATEGORY_THROAT_VALUE),
        (CATEGORY_VITAMINE_KEY, CATEGORY_VITAMINE_VALUE),
        (CATEGORY_BAA_KEY, CATEGORY_BAA_VALUE),
    )
    name = models.CharField(verbose_name='Название препарата', max_length=500)
    photo = models.FileField(verbose_name='Фото', blank=True, null=True)
    price = models.FloatField(verbose_name='Цена', null=True)
    category = models.IntegerField(choices=CATEGORIES, default=CATEGORY_EMPTY_KEY, verbose_name='Категория')
    expiration_date = models.DateField(null=True)
    status = models.BooleanField(default=True, verbose_name='Активен')
    comment = models.CharField(verbose_name='Комментарий', max_length=500, blank=True, null=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', null=True, auto_now=True)

    def __str__(self):
        return self.name
