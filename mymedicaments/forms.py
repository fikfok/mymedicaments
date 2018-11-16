from django import forms
from django.forms import NumberInput, TextInput, FileField, RadioSelect

from mymedicaments.models import Medicament


class MedicamentForm(forms.ModelForm):

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
        photo_face = cleaned_data.get('photo_face')
        category = cleaned_data.get('category')

        if not name and not photo_face:
            msg = 'Необходимо ввести название или сделать снимок упаковки'
            self.add_error('name', msg)
            self.add_error('photo_face', msg)

        if category.name == 'Пусто':
            msg = 'Необходимо указать категорию'
            self.add_error('category', msg)