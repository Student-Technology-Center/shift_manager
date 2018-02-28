from ..models import ShiftHelper, ShiftPlacement

def get_leader():
	shift_helpers = ShiftHelper.objects.all()

	if shift_helpers.count() > 1:
		return False
	else:
		return shift_helpers[0]

	return False

def switch_next_user():
	lead = get_leader()

	if lead.current_place >= lead.max_place - 1:
		print("first")
		lead.going_up = False

	if lead.current_place <= 0:
		print("second")
		lead.going_up = True

	if lead.going_up:
		print("third")
		lead.current_place += 1

	if not lead.going_up:
		print("fourth")
		lead.current_place -= 1

	lead.save()

	shift = ShiftPlacement.objects.get(user=lead.current_user)
	shift.amt_left = lead.shifts_per_turn
	shift.save()

	user = ShiftPlacement.objects.get(place=lead.current_place).user
	print("New user {} (Place: {})".format(user.username, user.shiftplacement.place))
	lead.current_user = user
	lead.save()

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
