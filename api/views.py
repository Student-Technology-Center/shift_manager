from django.http import JsonResponse
from django.conf import settings

def creating_shift(request):
	return JsonResponse({
			'creating_shifts' : str(settings.CREATING_SHIFTS)
		})