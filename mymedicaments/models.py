from django.db import models


class Medicament(models.Model):
    name = models.CharField(verbose_name='Название препарата', max_length=500)
    photo = models.ImageField(upload_to='products')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')

    def __str__(self):
        return self.name