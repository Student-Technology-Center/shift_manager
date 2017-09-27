from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import IntegrityError

from shiftmanager.models import ShiftPlacement, ShiftForm

import random

def index(request):
    user_model = get_user_model()

    context = {}
    context["creating_shifts"] = settings.CREATING_SHIFTS;

    if not context['creating_shifts']:
        if request.method == 'POST' and request.POST.get('create_shifts', False) and request.user.is_superuser:
<<<<<<< HEAD
            num_of_users = len([x for x in request.POST.keys() if request.POST.get(x, False) == 'on'])
=======
            settings.USER_SHIFT_PLACE = 1
            user_list = [x for x in request.POST.keys() if request.POST.get(x, False) == 'on']
            user_obj_list = [user_model.objects.get(username=x) for x in user_list]
            num_of_users = len(user_list)

>>>>>>> bfcb171d83593e4f97014937ac44b3b76cb7167d
            if num_of_users == 0:
                context['no_users'] = True
                return render(
                    request,
                    'shift_index.html',
                    context
                )

            for user in user_obj_list:
                user.shiftplacement.order = 0
                user.shiftplacement.save()
            
            list_of_placement = random.sample(range(1, num_of_users + 1), num_of_users)

            for index, user in enumerate(user_obj_list):
                user.shiftplacement.order = list_of_placement[index]
                user.shiftplacement.save()

<<<<<<< HEAD
                    while rand_num in user_num_list:
                        rand_num = randint(0, num_of_users - 1)
                    
                    user_num_list.append(rand_num)
                    try:
                        settings_obj[0].order = rand_num
                        settings_obj[0].save()
                    except IntegrityError:
                        pass
            settings.NUM_USERS = num_of_users
=======
>>>>>>> bfcb171d83593e4f97014937ac44b3b76cb7167d
            settings.CREATING_SHIFTS = True
            settings.USER_SHIFT_PLACE = 0
            return redirect('/shifts/create/')

    context['user_list'] = user_model.objects.all()
    
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
    context['shift_form'] = ShiftForm(None)

    user_model = get_user_model()
    if not context['creating_shifts']:
        return redirect('/shifts/')
    context['starting_place'] = settings.USER_SHIFT_PLACE
    context['current_user'] = ShiftPlacement.objects.get(order=settings.USER_SHIFT_PLACE).user

    return render(
            request,
            'creating_shifts.html',
            context
        )
