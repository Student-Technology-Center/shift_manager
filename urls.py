from django.conf.urls import url

import shiftmanager.views as shift_views

urlpatterns = [
    url('^$', shift_views.index, name='index')
]