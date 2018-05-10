from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import ShiftHelper, Shift, ShiftPlacement
from . import view_helpers

from datetime import datetime, time, timedelta
from math import floor, ceil

from .. models import ShiftFile

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
	turns = request.GET.get('turns', 0)

	if type(turns) == str:
		try:
			turns = int(turns)
		except ValueError:
			return JsonResponse({"failed":"If using turns GET parameter, please input a valid integer."})

	leader = view_helpers.get_leader()
	rounds_skipped = floor(turns / leader.max_place)
	turns %= leader.max_place - 1
	direction = None

	if (rounds_skipped % 2) == 0:
		direction = leader.going_up
	else:
		direction = not leader.going_up

	if direction:
		turn = leader.current_place + turns
		if (turn >= leader.max_place):
			turn -= floor(turns / 2)
	else:
		turn = leader.current_place - turns
		if (turn < 0):
			turn += floor(turns / 2)

	print(leader.current_place)
	print(turn)

	return JsonResponse({"main_user": "someone"})

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

	if len(shifts) == 0:
		return JsonResponse({
			{}
		})

	context['success'] = [{
		'datetime' : datetime.strptime("{} {}".format(shift.date, shift.start), '%Y-%m-%d %H:%M:%S'),
		'name': "{} {}".format(shift.user.first_name, shift.user.last_name),
		'day_of_week':shift.day_of_week
	} for shift in shifts if shift.user != None]

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

	for load in loads:
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

	return JsonResponse({"details":"An error has occurred, make sure payload info is correct"}, json_dumps_params={'indent': 2})

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

