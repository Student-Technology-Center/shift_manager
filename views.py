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

        #Remove all previous shifts.
        for shift in shifts:
            shift.delete()

        for user in context['user_list']:
            if request.POST.get(user.username, False):
                current_user = get_user_model().objects.get(username=user.username)
                new_placement = ShiftPlacement.objects.create(user=current_user, order=order[order_place])
                order_place += 1

        return redirect('/shifts/create/')

    return render(
        request,
        "shift_index.html",
        context
    )

def create(request):
    context = { }
    context['order'] = []
    all_shifts = list(ShiftPlacement.objects.all())

    for value, user in enumerate(all_shifts):
        current_shift = ShiftPlacement.objects.get()

    people = get_user_model().objects.all()

    return render(
        request,
        "shift_create.html",
        context
    )
