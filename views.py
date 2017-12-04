from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import IntegrityError

from shiftmanager.models import ShiftPlacement, ShiftForm, ShiftHelper

import random

def index(request):
    context = { }

    context['user_list'] = get_user_model().objects.all()
    number_of_users = 0

    if request.method == 'POST':
        for user in context['user_list']:
            if request.POST.get(user.username, False):
                number_of_users += 1

        order = random.sample(range(0, number_of_users), number_of_users)
        order_place = 0
        shifts = ShiftPlacement.objects.all()
        shift_helper = ShiftHelper.objects.all()

        #Remove the shift helper, this should only go once,
        #but for sake of future proofing..
        for helper in shift_helper:
            helper.delete()

        #Remove all previous shifts.
        for shift in shifts:
            shift.delete()

        for user in context['user_list']:
            if request.POST.get(user.username, False):
                current_user = get_user_model().objects.get(username=user.username)
                new_placement = ShiftPlacement.objects.create(user=current_user, order=order[order_place])
                order_place += 1

        new_shift = ShiftHelper.objects.create()
        new_shift.pk = request.user.pk
        new_shift.save()

        return redirect('/shifts/create/')

    return render(
        request,
        "shift_index.html",
        context
    )


def create(request):

    context = { }

    users = ShiftPlacement.objects.all()
    amt_of_users = len(users)
    ordered_list_of_users = []
    
    for i in range(0, amt_of_users):
        ordered_list_of_users.append(ShiftPlacement.objects.get(order=i))

    context['order'] = ordered_list_of_users
    context['current_user'] = ShiftPlacement.objects.get(order=ShiftHelper.objects.get(pk=request.user.pk).current_place)

    return render(
        request,
        "shift_create.html",
        context
    )
