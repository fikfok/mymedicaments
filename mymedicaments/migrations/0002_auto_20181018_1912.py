# Generated by Django 2.1.2 on 2018-10-18 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mymedicaments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicament',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicament',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='medicament',
            name='price',
            field=models.FloatField(null=True, verbose_name='Цена'),
        ),
    ]
