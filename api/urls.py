from django.conf.urls import url

import shiftmanager.api.views as views

#user related shifts
urlpatterns = [
	url(r'get_shifts/$', views.get_shifts)
]