from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import IntegrityError

from shiftmanager.models import ShiftFile, Shift
from utils.message import send_stc_email
from login.models import UserOptions

from .forms import ShiftExcelUpload
from .helpers import claim_shifts

import random

'''
    This view exists as a solution to
    get the shifts onto our website.
    I never finished Shift Manager, but
    I have left my code in-case you are
    brave enough to finish it. For now,
    you simply upload an excel document
    in David's format and it'll scrape it for the shifts.
'''
def file_upload(request):
    if request.POST:
        form = ShiftExcelUpload(request.POST, request.FILES)
        if form.is_valid():
            new_f = form.save(commit=False)
            new_f.user = request.user
            new_f.save()
    else:
        form = ShiftExcelUpload()

    context = { 
        "form"  : form, 
        "sheets": ShiftFile.objects.all()
    }

    return render(
        request,
        "shift_upload.html",
        context
    )

#Temporary fix, just calls the helper function
#to assign shifts to people.
def assign_shifts(request):
    claim_shifts(request)
    return redirect('/shifts/')

def remove(request, pk):
    if request.user.is_superuser:
        item = ShiftFile.objects.get(pk=pk)
        item.delete()

    return redirect('/shifts/')