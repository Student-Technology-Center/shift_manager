from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.conf import settings

import datetime
from shiftmanager.models import Shift, ShiftPlacement, ShiftHelper

#Create a shift

#Future TODO

'''
	There is too much logic shoved into something called
	create_shift, really there should be a few more API 
	endpoints for deleting shifts and such.

	This is definitely something that needs cleaning up,
	and was obviously a bit rushed.

	FUTURE ENDPOINTS:
		- Create
		- Delete
		- Interject
'''
def create_shift(request):
	shift_create = { }

	#Really not sure why javascript sends it like string[string], tried to fix.
	shift_create['username'] = request.POST.get('payload[username]', False)
	shift_create['start_time'] = request.POST.get('payload[timeStart]', False)
	shift_create['dow'] = request.POST.get('payload[dow]', False)
	shift_create['action'] = request.POST.get('payload[action]', False)
	chose_to_pass = request.POST.get('pass', False)

	if shift_create['username']:
		user = get_user_model().objects.get(username=shift_create['username'])

		#Uses the string to create the start time, this is normal, don't change it.
		time_start_obj = datetime.datetime.strptime(shift_create['start_time'], '%H:%M').time()

		#Gets an hour from the start time
		time_end_obj = (datetime.datetime.strptime(shift_create['start_time'], '%H:%M') + datetime.timedelta(hours=1)).time()
	else:
		user = get_user_model().objects.get(username=request.POST.get('pass'))

	shift_placement = ShiftPlacement.objects.get(user=user)

	if chose_to_pass:
		shift_helper = ShiftHelper.objects.get(pk=request.user.pk)
		shift_placement.amt_per_turn += shift_helper.amt_per_turn
		if (shift_helper.adding):
			shift_helper.current_place += 1
		else:
			shift_helper.current_place -= 1

		if (shift_helper.current_place == shift_helper.total_amt):
			shift_helper.adding = False
			shift_helper.current_place -= 1

		if (shift_helper.current_place == -1):
			shift_helper.adding = True
			shift_helper.current_place += 1

		shift_helper.save()
		shift_placement.save()

		next_user = ShiftPlacement.objects.get(order=ShiftHelper.objects.get(pk=request.user.pk).current_place)

		return JsonResponse({
				'status' : 'success',
				'message' : 'Shifts received.',
				'next_user': next_user.user.username,
				'first': next_user.user.first_name,
				'last': next_user.user.last_name,
				'current_username':shift_placement.user.username,
				'turns_left_current': shift_placement.amt_per_turn,
				'hours_current': len(Shift.objects.filter(user=user)),
				'action':'create'
		})

	for entry in shift_create.keys():
		if (not shift_create[entry]):
			print("Something went wrong when creating a shift - a field was missing.")
			return


	if shift_create['action'] == 'create':
		shift = Shift.objects.filter(user=user,start=time_start_obj, day_of_week=shift_create['dow'])

		if len(shift) != 0:
			return JsonResponse({
				'status' : 'failure',
				'message' : "You're already working this shift."
			})

		shift_helper = ShiftHelper.objects.get(pk=request.user.pk)
		amt_left = shift_placement.amt_per_turn - 1
		shift_placement.amt_per_turn = amt_left
		switching = False

		#Should only happen once a user has
		#forced end of turn to bank, or has filled in
		#all their shifts.
		if amt_left == 0:
			shift_placement.amt_per_turn += shift_helper.amt_per_turn
			if (shift_helper.adding):
				shift_helper.current_place += 1
			else:
				shift_helper.current_place -= 1

			if (shift_helper.current_place == shift_helper.total_amt):
				shift_helper.adding = False
				shift_helper.current_place -= 1

			if  (shift_helper.current_place == -1):
				shift_helper.adding = True
				shift_helper.current_place += 1

		shift_helper.save()
		shift_placement.save()

		new_shift = Shift.objects.create(day_of_week=shift_create['dow'],
										 start=time_start_obj,
										 end=time_end_obj,
										 user=user)

		print("We are currently on person {}, we are going {}, the max is {}..".format(shift_helper.current_place, 
			"forward" if shift_helper.adding else "backwards",
				shift_helper.total_amt))

		next_user = ShiftPlacement.objects.get(order=ShiftHelper.objects.get(pk=request.user.pk).current_place)

		return JsonResponse({
				'status' : 'success',
				'message' : 'Shifts received.',
				'next_user': next_user.user.username,
				'first': next_user.user.first_name,
				'last': next_user.user.last_name,
				'switch': switching,
				'current_username':shift_placement.user.username,
				'turns_left_current': shift_placement.amt_per_turn,
				'hours_current': len(Shift.objects.filter(user=user)),
				'action':'create'
		})

	if shift_create['action'] == 'delete':
		shift = Shift.objects.filter(user=user, start=time_start_obj, day_of_week=shift_create['dow'])
		for i in shift:
			shift_pl = ShiftPlacement.objects.get(user=user)
			shift_pl.amt_per_turn += 1
			shift_pl.save()
			i.delete()

		return JsonResponse({
				'status':'success',
				'message':'Shifts deleted.',
				'username':user.username,
				'turns_left_current':shift_pl.amt_per_turn,
				'hours_current': len(Shift.objects.filter(user=user)),
				'action':'delete'
		})

	return JsonResponse({
			'status':'failure',
			'message':'Fell through conditions.'
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
			user = shift.user
			shift_pl = ShiftPlacement.objects.get(user=shift.user)
			shift_pl.amt_per_turn += 1
			shift_pl.save()
			shift.delete()

	return JsonResponse({
		'status':'success',
		'message':'All shifts deleted.',
		'action':'delete'
	})

def add_hours_to_user(request):
	if request.user.is_superuser:
		hours = request.GET.get('hours', False)
		username = request.GET.get('username', False)
		if hours and username:
			user = get_user_model().objects.get(username=username)
			shift_placement = ShiftPlacement.objects.get(user=user)
			try:
				shift_placement.amt_per_turn += int(hours)
			except:
				return JsonResponse({
					'status':'failure',
					'message':'Could not convert hours'
				})
			shift_placement.save()
			return JsonResponse({
				'status':'success',
				'message':'Hours added',
				'new_amt':shift_placement.amt_per_turn
			})
	return JsonResponse({
		'status':'failure',
		'message':'Could not convert hours'
	})
