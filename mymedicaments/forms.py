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
            'status'
        ]
        widgets = {
            'status': RadioSelect,
        }