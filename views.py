from django.shortcuts import render
from django.contrib.auth import get_user_model
import shiftmanager.settings

def index(request):
    user_model = get_user_model()

    context = {}
    context["creating_shifts"] = shiftmanager.settings.CREATING_SHIFTS;
    context['user_list'] = user_model.objects.all()

    if request.method == 'POST' and request.POST.get('create_shifts', False):
        for user in request.POST.keys():
            if request.POST.get(user, False) == 'on':
                curr_user = user_model.objects.get(username=user)
                print(curr_user.first_name)

    return render(
        request,
        'shift_index.html',
        context
    )
