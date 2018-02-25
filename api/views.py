from django.http import JsonResponse
from django.contrib.auth import get_user_model
from ..models import ShiftHelper, Shift, ShiftPlacement
from . import view_helpers

from datetime import datetime, time, timedelta

'''
	User based views
'''
def get_leader(request):

	helpers = ShiftHelper.objects.all()

	if helpers.count() > 1:
		return JsonResponse({"details":"Got more than one helper."})

	return JsonResponse({"details":"{}".format(helpers[0].owner.username)})

def check_leader(request):
	user = request.user
	opt_user = request.GET.get('username', False)

	if opt_user:
		if get_user_model().objects.filter(username=opt_user).exists():
			user = get_user_model().objects.get(username=opt_user)

	if ShiftHelper.objects.filter(owner=user).exists():
		return JsonResponse({"details":"True"})

	return JsonResponse({"details":"False"})

def get_turn_user(request):
	return JsonResponse({"main_user": request.user.shifthelper.current_user.username})

def set_turn_user(request):
	username = request.POST.get('username', False)
	user_exists = False

	if username:
		user_exists = get_user_model().objects.filter(username=username).exists()

	if user_exists:
		request.user.shifthelper.current_user = get_user_model().objects.get(username=username)
		return JsonResponse({"details":"User has been set."})

	return JsonResponse({"details":"An error has occurred."})

'''
	TODO: Flesh out into richer API
'''
def get_shifts(request):
	context = {}

	context['details'] = [{
		'start':str(shift.start),
		'end':str(shift.end),
		'date':str(shift.date),
		'datetime' : datetime.strptime("{} {}".format(shift.date, shift.start), '%Y-%m-%d %H:%M:%S'),
		'name': "{} {}".format(shift.user.first_name, shift.user.last_name),
		'day_of_week':shift.day_of_week,
		'up_for_grabs':shift.up_for_grabs,
	} for shift in Shift.objects.all()]

	return JsonResponse(context, json_dumps_params={'indent': 2})

'''
	Payload based views
'''
def receive_payloads(request):
	action = request.POST.get('action', False)
	dow = request.POST.get('dow', False)
	start_time = request.POST.get('time_start', False)

	if not action or not dow or not start_time:
		return JsonResponse({"details":"Missing information"})

	if action == 'create':
		return handle_creation(dow, start_time)

	if action == 'delete':
		return handle_deletion(dow, start_time)

	return JsonResponse({"details":"An error has occurred, make sure payload info is correct"})

'''
	Returns a JsonResponse for creating a shift
'''
def handle_creation(dow, start_time):

	lead = view_helpers.get_leader()

	if not lead:
		return JsonResponse({'failed':"Could't create user object."})

	user = lead.current_user
	shift_stats = ShiftPlacement.objects.get(user=user)

	s = datetime.strptime(start_time, '%H:%M')
	e = s + timedelta(hours=1)

	start = s.time()
	end = e.time()

	delta = view_helpers.get_leader().end_date - view_helpers.get_leader().start_date
	dates = [view_helpers.get_leader().start_date + timedelta(days=date) for date in range(delta.days + 1)]

	for date in dates:
		if view_helpers.weekday_lookup(date.weekday()) == dow:
			new_shift = Shift.objects.create(day_of_week=dow,
												start=start,
												end=end,
												user=user)
			new_shift.date = date
			new_shift.save()

	shift_stats.amt_left -= 1
	shift_stats.save()

	if shift_stats.amt_left <= 0:
		view_helpers.switch_next_user()

	return JsonResponse({"success":"Shift was created."})

def delete_all(request):

	if not request.user.is_superuser:
		return JsonResponse({"failed":"Not admin."})

	for i in Shift.objects.all():
		i.delete()

	return JsonResponse({"success":"Deleted ALL shifts."})
'''
	Returns a JsonResponse for deleting a shift
'''
def handle_deletion(dow, start_time):
	return JsonResponse({"details":"Deleting!"})

