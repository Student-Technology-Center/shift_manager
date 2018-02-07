from django.http import JsonResponse
from django.contrib.auth import get_user_model
from ..models import ShiftHelper

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
	Payload based views
'''
def receive_payloads(request):
	action = request.POST.get('payload[action]', False)
	dow = request.POST.get('payload[dow]', False)
	start_time = request.POST.get('payload[timeStart]', False)

	print(action)
	print(dow)
	print(start_time)

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
	return JsonResponse({"details":"Creating!"})


'''
	Returns a JsonResponse for deleting a shift
'''
def handle_deletion(dow, start_time):
	return JsonResponse({"details":"Deleting!"})

