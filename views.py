from django.shortcuts import render
from django.contrib.auth import get_user_model
import shiftmanager.settings

def index(request):
    context = {}
    context["creating_shifts"] = shiftmanager.settings.CREATING_SHIFTS;

    context['user_list'] = get_user_model().objects.all()

    return render(
        request,
        'shift_index.html',
        context
    )
