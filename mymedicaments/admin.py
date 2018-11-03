from django.contrib import admin
from mymedicaments.models import Category, Medicament, Status


admin.site.register(Medicament)
admin.site.register(Category)
admin.site.register(Status)

