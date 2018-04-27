from django.conf.urls import url, include

import shiftmanager.views as shift_views

urlpatterns = [
    url(r'^$', shift_views.file_upload, name='index'),
    url(r'^create/$', shift_views.create, name='create'),
    url(r'^remove/(?P<pk>\d+)/$', shift_views.remove, name='remove'),
    url(r'^upload/$', shift_views.file_upload, name='upload')
]

#Commented out for now, since it's not needed.
# #api
# urlpatterns += [
# 	url(r'api/', include('shiftmanager.api.urls', namespace='api'))
# ]