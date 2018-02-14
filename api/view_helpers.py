from ..models import ShiftHelper

def get_leader():
	shift_helpers = ShiftHelper.objects.all()

	if shift_helpers.count() > 1:
		return False
	else:
		return shift_helpers[0]

	return False
