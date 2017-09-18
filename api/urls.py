from django.conf.urls import url

import shiftmanager.api.views as views

urlpatterns = [
	url(r'creating/', views.creating_shift, name='creating_shift')
]