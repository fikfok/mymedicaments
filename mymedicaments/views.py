import copy
import datetime
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
    ACTIVE = 0
    NOT_ACTIVE = 1

    base_url = request.build_absolute_uri().replace(request.get_full_path(), '')
    active_status_id = Status.objects.get(name='Активен').pk
    active_medicaments = Medicament.objects.\
        annotate(created_date=Func(F('created_at'), function='DATE')). \
        annotate(
            new_status=Case(
                When(status=active_status_id, then=Value(ACTIVE)),
                default=Value(NOT_ACTIVE),
                output_field=IntegerField()
            )).\
        filter(author=request.user, new_status=ACTIVE). \
        order_by('-created_date', '-pk')

    not_active_medicaments = Medicament.objects.\
        annotate(created_date=Func(F('created_at'), function='DATE')). \
        annotate(
            new_status=Case(
                When(status=active_status_id, then=Value(ACTIVE)),
                default=Value(NOT_ACTIVE),
                output_field=IntegerField()
            )).\
        filter(author=request.user, new_status=NOT_ACTIVE). \
        order_by('-created_date', 'name')

    total_dataset = list(active_medicaments) + list(not_active_medicaments)

    data = {'data': [
        [
            item.pk,
            item.name,
            item.price,
            item.category.name,
            base_url + item.photo_face.url_small if item.photo_face.name else None,
            base_url + item.photo_date.url_small if item.photo_date.name else None,
            base_url + item.photo_recipe.url_small if item.photo_recipe.name else None,
            item.created_date.strftime('%d.%m.%Y'),
            item.expiration_date.strftime('%d.%m.%Y') if item.expiration_date else None,
            item.opening_date.strftime('%d.%m.%Y') if item.opening_date else None,
            item.use_up_date.strftime('%d.%m.%Y') if item.use_up_date else None,
            item.result.name if item.result else None,
            item.comment,
            item.status.name,
            True if item.status_id == active_status_id else False,
            None
        ]
        for item in total_dataset
    ]}
    return JsonResponse(data, safe=False)


@login_required
def save_medicament(request):
    if request.method == 'POST':
        data = {}
        post_data = copy.deepcopy(request.POST)
        form = MedicamentForm(data=post_data, files=request.FILES)
        if form.is_valid():
            medicament = form.save(commit=False)
            medicament.author = request.user
            medicament.save()
            data['status'] = 'ok'
        else:
            data['status'] = 'error'
            data['errors'] = [{'field_name': error[0], 'message': error[1][0]} for error in list(form.errors.items())]
    return JsonResponse(data, safe=False)


@login_required
def get_categories(request):
    data = list(Category.objects.all().order_by('name').values_list('pk', 'name'))
    return JsonResponse(data, safe=False)


@login_required
def update_medicament(request, medicament_id):
    data = {}
    if request.method == 'POST':
        medicament = get_object_or_404(Medicament, pk=medicament_id, author=request.user)
        if 'used_up' in request.POST:
            medicament.status = Status.objects.get(name='Израсходован')
            medicament.save()
            data['status'] = 'ok'
        else:
            form = MedicamentForm(data=request.POST, files=request.FILES, instance=medicament)
            if form.is_valid():
                medicament.save()
                data['status'] = 'ok'
            else:
                data['status'] = 'error'
                data['errors'] = [{'field_name': error[0], 'message': error[1][0]} for error in list(form.errors.items())]
    return JsonResponse(data, safe=False)


@login_required
def get_medicament_data(request, medicament_id):
    base_url = request.build_absolute_uri().replace(request.get_full_path(), '')
    medicament_data = Medicament.objects.\
        annotate(created_date=Func(F('created_at'), function='DATE')). \
        get(author=request.user, pk=medicament_id)

    data = {
        'pk': medicament_data.pk,
        'name': medicament_data.name,
        'price': medicament_data.price,
        'category': medicament_data.category.pk,
        'photo_face': base_url + medicament_data.photo_face.url if medicament_data.photo_face.name else None,
        'photo_date': base_url + medicament_data.photo_date.url if medicament_data.photo_date.name else None,
        'photo_recipe': base_url + medicament_data.photo_recipe.url if medicament_data.photo_recipe.name else None,
        'created_date': medicament_data.created_date.strftime('%d.%m.%Y'),
        'expiration_date': medicament_data.expiration_date.strftime('%d.%m.%Y') if medicament_data.expiration_date else None,
        'opening_date': medicament_data.opening_date.strftime('%d.%m.%Y') if medicament_data.opening_date else None,
        'use_up_date': medicament_data.use_up_date.strftime('%d.%m.%Y') if medicament_data.use_up_date else None,
        'result': medicament_data.result.name if medicament_data.result else None,
        'comment': medicament_data.comment,
        'status': medicament_data.status.name
    }
    return JsonResponse(data, safe=False)
