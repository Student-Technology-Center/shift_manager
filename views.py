from django.shortcuts import render

def index(request):
    context = {}

    return render(
        request,
        'shift_index.html',
        context
    )
