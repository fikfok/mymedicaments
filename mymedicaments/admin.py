from django.contrib import admin
from mymedicaments.models import Category, Medicament, Status, Result


admin.site.register(Medicament)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Result)
