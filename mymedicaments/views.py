import os
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from django.db.models import Func, F

from mymedicaments.models import Category, Medicament, Status
from mymedicaments.forms import MedicamentForm

def home(request):
    return render(request, 'home.html', context={})


@login_required
def get_medicaments(request):
    base_url = request.build_absolute_uri().replace(request.get_full_path(), '')

    medicaments = Medicament.objects.\
        annotate(created_date=Func(F('created_at'), function='DATE')).\
        filter(author=request.user).order_by('-created_date', 'name')

    data = {'data': [
        [
            item.name,
            item.price,
            item.category.name,
            base_url + item.photo_face.url if item.photo_face.name else None,
            base_url + item.photo_date.url if item.photo_date.name else None,
            base_url + item.photo_recipe.url if item.photo_recipe.name else None,
            item.created_date.strftime('%d.%m.%Y'),
            item.expiration_date.strftime('%d.%m.%Y') if item.expiration_date else None,
            item.comment,
            item.status.name,
            None
        ]
        for item in medicaments
    ]}
    return JsonResponse(data, safe=False)


@login_required
def save_medicament(request):
    if request.method == 'POST':
        path = settings.MEDIA_ROOT + '/'
        file_name = str(uuid.uuid4())

        photo_file = request.FILES['photo']
        path = path + '/'
        ext = os.path.splitext(photo_file.name)[-1].lower()
        absolut_path = path + file_name + ext
        destination = open(absolut_path, 'wb+')
        for chunk in photo_file.chunks():
            destination.write(chunk)
        destination.close()

        form = MedicamentForm(request.POST)
        medicament = form.save(commit=False)
        medicament.photo_face = file_name + ext
        medicament.author = request.user
        medicament.save()
    return JsonResponse({}, safe=False)


@login_required
def get_categories(request):
    data = list(Category.objects.all().order_by('name').values_list('pk', 'name'))
    # data = sorted(data, key=lambda item: item[1])
    return JsonResponse(data, safe=False)
