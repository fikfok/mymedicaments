import os
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render

from mymedicaments.models import Medicament
from mymedicaments.forms import MedicamentForm

def home(request):
    return render(request, 'home.html', context={})


@login_required
def get_medicaments(request):
    base_url = request.build_absolute_uri().replace(request.get_full_path(), '')

    medicaments = Medicament.objects.filter(author=request.user)

    data = {'data': [
        [
            item.name,
            item.price,
            base_url + item.photo.url
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
        medicament.photo = file_name + ext
        medicament.author = request.user
        medicament.save()
    return JsonResponse({}, safe=False)
