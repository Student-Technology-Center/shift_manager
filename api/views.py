from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.conf import settings

import datetime
from shiftmanager.models import Shift, ShiftPlacement, ShiftHelper

#Create a shift
def create_shift(request):
	shift_create = { }

	#Really not sure why javascript sends it like string[string], tried to fix.
	shift_create['username'] = request.POST.get('payload[username]', False)
	shift_create['start_time'] = request.POST.get('payload[timeStart]', False)
	shift_create['dow'] = request.POST.get('payload[dow]', False)
	shift_create['action'] = request.POST.get('payload[action]', False)

	for entry in shift_create.keys():
		if (not shift_create[entry]):
			print("Something went wrong when creating a shift - a field was missing.")
			return

	user = get_user_model().objects.get(username=shift_create['username'])

	#Uses the string to create the start time, this is normal, don't change it.
	time_start_obj = datetime.datetime.strptime(shift_create['start_time'], '%H:%M').time()

	#Gets an hour from the start time
	time_end_obj = (datetime.datetime.strptime(shift_create['start_time'], '%H:%M') + datetime.timedelta(hours=1)).time()

	if shift_create['action'] == 'create':
		shift = Shift.objects.filter(user=user,start=time_start_obj, day_of_week=shift_create['dow'])

		if len(shift) != 0:
			return JsonResponse({
				'status' : 'failure',
				'message' : "You're already working this shift."
			})

		shift_helper = ShiftHelper.objects.get(pk=request.user.pk)

		#Should only happen once a user has
		#forced end of turn to bank, or has filled in
		#all their shifts.
		if (shift_helper.adding):
			print("Going forwards")
			shift_helper.current_place += 1
		else:
			print("going back")
			shift_helper.current_place -= 1

		if (shift_helper.current_place == shift_helper.total_amt):
			shift_helper.adding = False
			shift_helper.current_place -= 1

		if  (shift_helper.current_place == -1):
			shift_helper.adding = True
			shift_helper.current_place += 1

		shift_helper.save()

		new_shift = Shift.objects.create(day_of_week=shift_create['dow'],
										 start=time_start_obj,
										 end=time_end_obj,
										 user=user)

		print("We are currently on person {}, we are going {}, the max is {}..".format(shift_helper.current_place, 
			"forward" if shift_helper.adding else "backwards",
				shift_helper.total_amt))

		next_user = ShiftPlacement.objects.get(order=ShiftHelper.objects.get(pk=request.user.pk).current_place).user
		print("Go {}!".format(next_user.username))

		return JsonResponse({
				'status' : 'success',
				'message' : 'Shifts received.',
				'next_user': ShiftPlacement.objects.get(order=ShiftHelper.objects.get(pk=request.user.pk).current_place).user.username,
				'first': next_user.first_name,
				'last': next_user.last_name
		})

	if shift_create['action'] == 'delete':
		shift = Shift.objects.filter(user=user, start=time_start_obj, day_of_week=shift_create['dow'])
		for i in shift:
			i.delete()

		return JsonResponse({
				'status' : 'success',
				'message' : 'Shifts deleted.'
		})


#View all shifts
def get_all_shifts(request):
	shifts = Shift.objects.all()

	counter = 0
	json_obj = { }
	for shift in shifts:
		json_obj['shift_{}'.format(counter)] = {
			"username":shift.user.username,
			"first_name":shift.user.first_name,
			"last_name":shift.user.last_name,
			"start":shift.start,
			"end":shift.end,
			"day_of_week":shift.day_of_week
		}
		counter += 1
	return JsonResponse(json_obj, safe=False)

def delete_all(request):
	if request.user.is_superuser:
		shifts = Shift.objects.all()
		for shift in shifts:
			shift.delete()

	return JsonResponse({
		'status':'success',
		'message':'All shifts deleted.'
	})
