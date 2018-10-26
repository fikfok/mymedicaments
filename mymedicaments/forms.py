from django import forms
from django.forms import NumberInput, TextInput, FileField

from mymedicaments.models import Medicament


class MedicamentForm(forms.ModelForm):

    class Meta:
        model = Medicament
        fields = ['name', 'price', 'photo']#, 'author'
