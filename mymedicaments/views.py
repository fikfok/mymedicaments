import json
import os
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Func, F, Case, Value, When, IntegerField

from mymedicaments.models import Category, Medicament, Status
from mymedicaments.forms import MedicamentForm


PATH = settings.MEDIA_ROOT + '/'


def home(request):
    return render(request, 'home.html', context={})


@login_required
def get_medicaments(request):
    base_url = request.build_absolute_uri().replace(request.get_full_path(), '')
    active_status_id = Status.objects.get(name='Активен').pk
    medicaments = Medicament.objects.\
        annotate(created_date=Func(F('created_at'), function='DATE')). \
        annotate(
            new_status=Case(
                When(status=active_status_id, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )). \
        filter(author=request.user).order_by('new_status', '-created_date', 'name')

    data = {'data': [
        [
            item.pk,
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
            True if item.status_id == active_status_id else False,
            None
        ]
        for item in medicaments
    ]}
    return JsonResponse(data, safe=False)


@login_required
def save_medicament(request):
    if request.method == 'POST':
        new_photo_face_name = save_photo_file(request_file=request.FILES['photo-face'])
        new_photo_date_name = save_photo_file(request_file=request.FILES['photo-date'])
        new_photo_recipe_name = save_photo_file(request_file=request.FILES['photo-recipe'])

        form = MedicamentForm(request.POST)
        medicament = form.save(commit=False)
        medicament.photo_face = new_photo_face_name
        medicament.photo_date = new_photo_date_name
        medicament.photo_recipe = new_photo_recipe_name
        medicament.author = request.user
        medicament.save()
    return JsonResponse({}, safe=False)


@login_required
def get_categories(request):
    data = list(Category.objects.all().order_by('name').values_list('pk', 'name'))
    return JsonResponse(data, safe=False)


@login_required
def update_medicament(request, medicament_id):
    if request.method == 'PATCH':
        medicament = get_object_or_404(Medicament, pk=medicament_id)
        data = json.loads(request.body.decode("utf-8"))
        if 'used_up' in data:
            medicament.status = Status.objects.get(name='Израсходован')
        medicament.save()
    return JsonResponse({}, safe=False)


def save_photo_file(request_file):
    file_name = str(uuid.uuid4())
    photo_face = request_file
    path = PATH + '/'
    ext = os.path.splitext(photo_face.name)[-1].lower()
    absolut_path = path + file_name + ext
    destination = open(absolut_path, 'wb+')
    for chunk in photo_face.chunks():
        destination.write(chunk)
    destination.close()
    return file_name + ext

