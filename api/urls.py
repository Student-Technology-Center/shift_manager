from django.conf.urls import url

import shiftmanager.api.views as views

#GETS
urlpatterns = [
	url(r'creating/', views.creating_shift, name='creating_shift')
]

#POSTS
urlpatterns += [
	url(r'add_shift/', views.add_shift, name='add_shift')
]