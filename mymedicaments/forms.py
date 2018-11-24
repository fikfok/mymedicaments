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
        return datetime.strptime(value, "%d.%m.%Y")


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

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        # photo_face = cleaned_data.get('photo_face')
        photo_face = self.files.get('photo_face')

        if not name and not photo_face:
            msg = 'Необходимо ввести название или сделать снимок упаковки'
            self.add_error('name', msg)
            self.add_error('photo_face', msg)

    def clean_photo_face(self):
        original_file_name = self.cleaned_data['photo_face']
        file_name = str(uuid.uuid4())
        photo_face = original_file_name
        path = PATH + '/'
        ext = os.path.splitext(photo_face.name)[-1].lower()
        absolut_path = path + file_name + ext
        destination = open(absolut_path, 'wb+')
        for chunk in photo_face.chunks():
            destination.write(chunk)
        destination.close()
        return file_name + ext
