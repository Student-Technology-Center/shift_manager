from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Shift

from datetime import datetime, time, timedelta
from math import floor, ceil

from .. models import ShiftFile

'''
	TODO: Flesh out into richer API
'''
def get_shifts(request):
	context = {}

	start = request.GET.get('start', False)
	end = request.GET.get('end', False)
	details = request.GET.get('details', False)

	if details:
		return JsonResponse({"details":"Specify a range with <start> and <end> the format YYYY-MM-DD" +
									   " or specify a username with <username>."}, json_dumps_params={'indent': 2})

	if type(start) == str:
		try:
			start = datetime.strptime(start, "%m-%d-%Y")
		except ValueError:
			return JsonResponse({'failed':"Couldn't parse date in start. Make sure it's a date string in form YYYY-MM-DD."}, json_dumps_params={'indent': 2})

	if type(end) == str:
		try:
			end = datetime.strptime(end, "%m-%d-%Y")
		except ValueError:
			return JsonResponse({'failed':"Couldn't parse date in end. Make sure it's a date string in form YYYY-MM-DD."}, json_dumps_params={'indent': 2})

	shift_start = Shift.objects.filter(date__gte=start)
	shift_end = Shift.objects.filter(date__lte=end)
	shifts = shift_start & shift_end

	username = request.GET.get('username', False)

	if username:
		user_set = Shift.objects.filter(user__username=username)
		shifts &= user_set


	context['success'] = []
	context['success'] = [{
		'datetime' : datetime.strptime("{} {}".format(shift.date, shift.start), '%Y-%m-%d %H:%M:%S'),
		'name': "{} {}".format(shift.user.first_name, shift.user.last_name),
		'day_of_week':shift.day_of_week
	} for shift in shifts if shift.user != None]

	return JsonResponse(context, json_dumps_params={'indent': 2})

def delete_all(request):
	if not request.user.is_superuser:
		return JsonResponse({"failed":"Not admin."})

	for i in Shift.objects.all():
		i.delete()

	return JsonResponse({"success":"Deleted ALL shifts."})
