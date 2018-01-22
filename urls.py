from django.conf.urls import url, include

import shiftmanager.views as shift_views

urlpatterns = [
    url(r'^$', shift_views.index, name='index'),
    url(r'^create/$', shift_views.create, name='create')
]

#api
'''
urlpatterns += [
	url(r'api/', include('shiftmanager.api.urls', namespace='api'))
]
'''