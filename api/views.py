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
	loads = []
	new_obj = {}

	for i in request.POST.keys():
		if 'payloads' not in i:
			continue

		if 'action' in i:
			new_obj['action'] = request.POST.get(i, False)

		if 'timeStart' in i:
			new_obj['timeStart'] = request.POST.get(i, False)

		if 'dow' in i:
			new_obj['dow'] = request.POST.get(i, False)

		if 'dow' in new_obj and 'action' in new_obj and 'timeStart' in new_obj:
			loads.append(new_obj)
			new_obj = {}

	leader = view_helpers.get_leader()
	shift_stats = ShiftPlacement.objects.get(user=leader.current_user)
	print("Entering a shift for {} (Place: {})".format(leader.current_user.username, shift_stats.place))

	for load in loads:
		print(shift_stats.amt_left)
		if load['action'] == 'create':
			handle_creation(load['dow'], load['timeStart'])
			shift_stats.amt_left -= 1
			shift_stats.save()

		if load['action'] == 'delete':
			handle_deletion(load['dow'], load['timeStart'])
			shift_stats.amt_left += 1
			shift_stats.save()

		if shift_stats.amt_left <= 0:
			view_helpers.switch_next_user()

	return JsonResponse({"details":"An error has occurred, make sure payload info is correct"})

'''
	Returns a JsonResponse for creating a shift
'''
def handle_creation(dow, start_time):

	lead = view_helpers.get_leader()

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
	pass

