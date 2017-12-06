from django.conf.urls import url

import shiftmanager.api.views as views

urlpatterns = [
	url(r'getallshifts/', views.get_all_shifts, name='getallshifts'),
	url(r'create/', views.create_shift, name='creating_shift'),
	url(r'deleteall/', views.delete_all, name='deleteall')
]