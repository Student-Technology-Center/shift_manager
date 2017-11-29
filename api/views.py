from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.conf import settings

from shiftmanager.models import Shift, ShiftPlacement

def creating_shift(request):
	return JsonResponse({
			'creating_shifts' : str(settings.CREATING_SHIFTS)
		})

def add_shift(request):
	user_model = get_user_model()
	if request.method == 'POST':
		shift_entry = Shift.objects.create(
			day_of_week=request.POST.get('day'),
			start=request.POST.get('start'),
			end=request.POST.get('end'),
			user=ShiftPlacement.objects.get(order=settings.USER_SHIFT_PLACE).user
		)

		settings.USER_SHIFT_PLACE += 1

		next_user = ShiftPlacement.objects.get(order=settings.USER_SHIFT_PLACE).user

		return JsonResponse({
			'status':'success',
			'first': str(next_user.first_name),
			'last': str(next_user.last_name),
			'place': str(settings.USER_SHIFT_PLACE)
		})
	else:
		return JsonResponse({
			'status':'Failed'
		})
