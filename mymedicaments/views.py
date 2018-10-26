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
        file_name = uuid.uuid4()
        form = MedicamentForm(request.POST, request.FILES)
        medicament = form.save(commit=False)
        medicament.author = request.user
        # form.fields['author'] = request.user
        medicament.save()
    return JsonResponse({}, safe=False)
