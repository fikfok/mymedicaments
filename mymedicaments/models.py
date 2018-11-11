from django.contrib.auth import get_user_model
from django.db import models


DEFAULT_CATEGORY = 1
DEFAULT_STATUS = 1


class Category(models.Model):
    name = models.CharField(verbose_name='Категория препарата', max_length=20)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(verbose_name='Категория препарата', max_length=20)

    def __str__(self):
        return self.name


class Result(models.Model):
    name = models.CharField(verbose_name='Результат приёма', max_length=50)

    def __str__(self):
        return self.name


class Medicament(models.Model):
    name = models.CharField(verbose_name='Название препарата', max_length=500)
    photo_face = models.FileField(verbose_name='Фото упаковки', blank=True, null=True)
    photo_date = models.FileField(verbose_name='Фото дат на упаковке', blank=True, null=True)
    photo_recipe = models.FileField(verbose_name='Фото рецепта', blank=True, null=True)
    price = models.FloatField(verbose_name='Цена', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=DEFAULT_CATEGORY, verbose_name='Категория', null=True, blank=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name='Результат приёма', null=True, blank=True)
    expiration_date = models.DateField(verbose_name='Годен до', blank=True, null=True)
    opening_date = models.DateField(verbose_name='Дата открытия', blank=True, null=True)
    use_up_date = models.DateField(verbose_name='Израсходовать до', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=DEFAULT_STATUS, verbose_name='Статус', blank=True, null=True)
    comment = models.CharField(verbose_name='Комментарий', max_length=500, blank=True, null=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', null=True, auto_now=True)

    def __str__(self):
        return self.name
