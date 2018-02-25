from django.conf.urls import url

import shiftmanager.api.views as views

#user related shifts
urlpatterns = [
	url(r'payload_dock/$', views.receive_payloads),
	url(r'get_leader/$', views.get_leader),
	url(r'check_leader/$', views.check_leader),
	url(r'get_turn_user/$', views.get_turn_user),
	url(r'set_turn_user/$', views.set_turn_user),
	url(r'get_shifts/$', views.get_shifts),
	url(r'erase_all_pictures_of_ron/$', views.delete_all),
]