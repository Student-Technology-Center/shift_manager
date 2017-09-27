from django.conf.urls import url

import shiftmanager.api.views as views

#GET
urlpatterns = [
	url(r'creating/', views.creating_shift, name='creating_shift')
]

#POST
urlpatterns += [
	url(r'add_shift/', views.add_shift, name='add_shift')
]