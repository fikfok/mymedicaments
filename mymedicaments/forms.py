import os
import uuid
from datetime import datetime

from django import forms
from django.forms import RadioSelect
from mymedicaments.models import Medicament
from django.conf import settings


PATH = settings.MEDIA_ROOT + '/'


class CustomDateField(forms.Field):
    def to_python(self, value):
        converted_date = None
        if value:
            converted_date = datetime.strptime(value, "%d.%m.%Y")
        return converted_date


class MedicamentForm(forms.ModelForm):

    expiration_date = CustomDateField()
    opening_date = CustomDateField()
    use_up_date = CustomDateField()

    class Meta:
        model = Medicament
        fields = [
            'name',
            'price',
            'category',
            'photo_face',
            'photo_date',
            'photo_recipe',
            'expiration_date',
            'comment',
            'status',
            'opening_date',
            'use_up_date',
            'result',
        ]
        widgets = {
            'status': RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expiration_date'].required = False
        self.fields['opening_date'].required = False
        self.fields['use_up_date'].required = False

    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')
        photo_face = self.files.get('photo_face')

        if not name and not photo_face:
            msg = 'Необходимо ввести название или сделать снимок упаковки'
            self.add_error('name', msg)
            self.add_error('photo_face', msg)
        return cleaned_data

    def clean_photo_face(self):
        new_file_name = None
        if self.cleaned_data['photo_face']:
            new_file_name = self._save_image(original_file_name=self.cleaned_data['photo_face'])
        return new_file_name

    def clean_photo_date(self):
        new_file_name = None
        if self.cleaned_data['photo_date']:
            new_file_name = self._save_image(original_file_name=self.cleaned_data['photo_date'])
        return new_file_name

    def clean_photo_recipe(self):
        new_file_name = None
        if self.cleaned_data['photo_recipe']:
            new_file_name = self._save_image(original_file_name=self.cleaned_data['photo_recipe'])
        return new_file_name

    def _save_image(self, original_file_name):
        new_file_name = str(uuid.uuid4())
        path = PATH
        ext = os.path.splitext(original_file_name.name)[-1].lower()
        original_file_name = new_file_name + ext
        absolut_path = path + original_file_name
        destination = open(absolut_path, 'wb+')
        for chunk in original_file_name.chunks():
            destination.write(chunk)
        destination.close()

        return original_file_name
