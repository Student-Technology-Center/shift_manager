from django.conf.urls import url, include

import shiftmanager.views as shift_views

urlpatterns = [
    url(r'^$', shift_views.file_upload, name='index'),
    url(r'^create/$', shift_views.create, name='create'),
    url(r'^upload/$', shift_views.file_upload, name='upload')
]

#api
urlpatterns += [
	url(r'api/', include('shiftmanager.api.urls', namespace='api'))
]