from django.db import models


class Medicament(models.Model):
    CATEGORY_EMPTY_KEY = 0
    CATEGORY_EMPTY_VALUE = 'Пусто'
    CATEGORY_NOSE_KEY = 1
    CATEGORY_NOSE_VALUE = 'Для носа'
    CATEGORY_THROAT_KEY = 2
    CATEGORY_THROAT_VALUE = 'Для горла'

    CATEGORIES = (
        (CATEGORY_EMPTY_KEY, CATEGORY_EMPTY_VALUE),
        (CATEGORY_NOSE_KEY, CATEGORY_NOSE_VALUE),
        (CATEGORY_THROAT_KEY, CATEGORY_THROAT_VALUE),
    )
    name = models.CharField(verbose_name='Название препарата', max_length=500)
    photo = models.FileField(verbose_name='Фото')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')
    category = models.IntegerField(choices=CATEGORIES, default=CATEGORY_EMPTY_KEY, verbose_name='Категория')
    expiration_date = models.DateTimeField(null=True)
    status = models.BooleanField(default=True, verbose_name='Активен')
    comment = models.CharField(verbose_name='Комментарий', max_length=500)

    def __str__(self):
        return self.name
