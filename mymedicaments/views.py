from django.http.response import JsonResponse
from django.shortcuts import render

from mymedicaments.models import Medicament


def home(request):
    return render(request, 'home.html', context={})


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
