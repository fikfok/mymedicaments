# Generated by Django 2.1.2 on 2018-11-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymedicaments', '0014_auto_20181103_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicament',
            name='opening_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата открытия'),
        ),
        migrations.AddField(
            model_name='medicament',
            name='use_up_date',
            field=models.DateField(blank=True, null=True, verbose_name='Израсходовать до'),
        ),
    ]
