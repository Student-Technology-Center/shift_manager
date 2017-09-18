from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import IntegrityError

from shiftmanager.models import ShiftPlacement
from random import randint

def index(request):
    user_model = get_user_model()

    context = {}
    context["creating_shifts"] = settings.CREATING_SHIFTS;
    context['user_list'] = user_model.objects.all()

    if not context['creating_shifts']:
        if request.method == 'POST' and request.POST.get('create_shifts', False) and request.user.is_superuser:
            num_of_users = len([x for x in request.POST.keys() if request.POST.get(x, False) == 'on'])

            if num_of_users == 0:
                context['no_users'] = True
                return render(
                    request,
                    'shift_index.html',
                    context
                )

            user_num_list = []
            for user in request.POST.keys():
                if request.POST.get(user, False) == 'on':
                    settings_obj = ShiftPlacement.objects.get_or_create(user=user_model.objects.get(username=user))
                    rand_num = randint(0, num_of_users - 1)

                    while rand_num in user_num_list:
                        rand_num = randint(0, num_of_users - 1)
                    
                    user_num_list.append(rand_num)
                    try:
                        settings_obj[0].order = rand_num
                        settings_obj[0].save()
                    except IntegrityError:
                        pass
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
    context['creating_shifts'] = settings.CREATING_SHIFTS

    if request.method == 'POST':
        settings.CREATING_SHIFTS = False
        return redirect('/shifts/')

    return render(
            request,
            'creating_shifts.html',
            context
        )
