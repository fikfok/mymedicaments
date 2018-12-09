from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from PIL import Image


DEFAULT_CATEGORY = 1
DEFAULT_STATUS = 1
SMALL_THUMB_SIZE = (60, 60)
MEDIUM_THUMB_SIZE = (200, 200)
PATH = settings.MEDIA_ROOT + '/'


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
    name = models.CharField(verbose_name='Название препарата', blank=True, null=True, max_length=500)
    photo_face = models.FileField(verbose_name='Фото упаковки оригинальный', blank=True, null=True)
    photo_face_small = models.FileField(verbose_name='Фото упаковки малый', blank=True, null=True)
    photo_face_medium = models.FileField(verbose_name='Фото упаковки средний', blank=True, null=True)

    photo_date = models.FileField(verbose_name='Фото дат на упаковке оригинальный', blank=True, null=True)
    photo_date_small = models.FileField(verbose_name='Фото дат на упаковке малый', blank=True, null=True)
    photo_date_medium = models.FileField(verbose_name='Фото дат на упаковке средний', blank=True, null=True)

    photo_recipe = models.FileField(verbose_name='Фото рецепта оригинальный', blank=True, null=True)
    photo_recipe_small = models.FileField(verbose_name='Фото рецепта малый', blank=True, null=True)
    photo_recipe_medium = models.FileField(verbose_name='Фото рецепта средний', blank=True, null=True)

    price = models.FloatField(verbose_name='Цена', blank=True, null=True)
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

    # def save_thumbnails(self):
    #     PATH = settings.MEDIA_ROOT + '/'
    #     original_image = Image.open(absolut_path)
    #     small_thumb = original_image.copy()
    #     small_thumb.thumbnail(SMALL_THUMB)
    #     small_file_name = new_file_name + '_small' + ext
    #     small_thumb_path = path + small_file_name
    #     small_thumb.save(small_thumb_path)
    #
    #     medium_thumb = original_image.copy()
    #     medium_thumb.thumbnail(MEDIUM_THUMB)
    #     medium_file_name = new_file_name + '_medium' + ext
    #     medium_thumb_path = path + medium_file_name
    #     medium_thumb.save(medium_thumb_path)


@receiver(pre_save, sender=Medicament)
def save_thumbnails(sender, instance, *args, **kwargs):
    """
    https://stackoverflow.com/questions/10840030/django-post-save-preventing-recursion-without-overriding-model-save
    """
    if not instance:
        return

    if hasattr(instance, '_dirty'):
        return

    if instance.photo_face:
        instance.photo_face_small = generate_thumbnail(instance.photo_face.name, SMALL_THUMB_SIZE, '_small')
        instance.photo_face_medium = generate_thumbnail(instance.photo_face.name, MEDIUM_THUMB_SIZE, '_medium')

    if instance.photo_date:
        instance.photo_date_small = generate_thumbnail(instance.photo_date.name, SMALL_THUMB_SIZE, '_small')
        instance.photo_date_medium = generate_thumbnail(instance.photo_date.name, MEDIUM_THUMB_SIZE, '_medium')

    if instance.photo_recipe:
        instance.photo_recipe_small = generate_thumbnail(instance.photo_recipe.name, SMALL_THUMB_SIZE, '_small')
        instance.photo_recipe_medium = generate_thumbnail(instance.photo_recipe.name, MEDIUM_THUMB_SIZE, '_medium')

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty


def generate_thumbnail(original_file_name, size, post_fix):
    ext = original_file_name.split('.')[-1].lower()
    saved_file_name = '.'.join(original_file_name.split('.')[:-1])
    absolut_path_to_saved_file = PATH + original_file_name

    original_image = Image.open(absolut_path_to_saved_file)
    thumb_image = original_image.copy()
    thumb_image.thumbnail(size)
    new_file_name = saved_file_name + post_fix + '.' + ext
    thumb_image_path = PATH + new_file_name
    thumb_image.save(thumb_image_path)
    return new_file_name