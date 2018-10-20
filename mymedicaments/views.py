from django.http.response import JsonResponse
from django.shortcuts import render

from mymedicaments.models import Medicament


def home(request):
    return render(request, 'home.html', context={})


def get_medicaments(request):
    medicaments = Medicament.objects.filter(author=request.user)
    data = [
        [
            item.name,
            item.price,
            item.photo.path
        ]
        for item in medicaments
    ]
    return JsonResponse(data, safe=False)
