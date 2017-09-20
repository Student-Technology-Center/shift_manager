from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import IntegrityError

from shiftmanager.models import ShiftPlacement, Shift, ShiftForm
import random

def index(request):
    user_model = get_user_model()

    context = {}
    context["creating_shifts"] = settings.CREATING_SHIFTS;
    context['user_list'] = user_model.objects.all()

    if request.method == 'POST' and request.POST.get('create_shifts', False) and request.user.is_superuser:
        user_list = [x for x in request.POST.keys() if request.POST.get(x, False) == 'on']
        num_of_users = len(user_list)

        if num_of_users == 0:
            context['no_users'] = True
            return render(
                request,
                'shift_index.html',
                context
            )

        user_num_list = random.sample(range(1, num_of_users + 1), num_of_users)

        for i, v in enumerate(user_list):
            settings_obj = ShiftPlacement.objects.get_or_create(user=user_model.objects.get(username=v))
            settings_obj[0].order = user_num_list[i]
            settings_obj[0].save()
            print('Gave {}, {}'.format(settings_obj[0].user.username, settings_obj[0].order))

        settings.CREATING_SHIFTS = True
        return redirect('/shifts/create/')
    
    if settings.CREATING_SHIFTS:
        return redirect('/shifts/create/')

    return render(
        request,
        'shift_index.html',
        context
    )

def shift_page(request):
    context = {}
    user_model = get_user_model()
    context['creating_shifts'] = settings.CREATING_SHIFTS
    context['shift_form'] = ShiftForm(None)

    if context['creating_shifts'] == False:
        return redirect(
            '/shifts/'
        )

    context['starting_user'] = ShiftPlacement.objects.get(order=settings.USER_SHIFT_PLACE).user

    return render(
            request,
            'creating_shifts.html',
            context
        )
