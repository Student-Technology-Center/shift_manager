from ..models import ShiftHelper, ShiftPlacement

def get_leader():
	shift_helpers = ShiftHelper.objects.all()

	if shift_helpers.count() > 1:
		return False
	else:
		return shift_helpers[0]

	return False

def get_next_user(x = 1):
	leader = get_leader()
	user = ShiftPlacement.objects.get(place=leader.current_place + x).user
	return user

def switch_next_user():
	user = view_helpers.get_next_user()
	lead = get_leader()
	#lead.current_user = user
	lead.save()
	print(lead.max_place)	

def weekday_lookup(day):
	if day == 0:
		return 'Mon'
	if day == 1:
		return 'Tue'
	if day == 2:
		return 'Wed'
	if day == 3:
		return 'Thu'
	if day == 4:
		return 'Fri'
	if day == 5:
		return 'Sat'
	if day == 6:
		return 'Sun'
	return False
