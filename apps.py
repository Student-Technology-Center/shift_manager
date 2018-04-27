from django.apps import AppConfig


class ShiftmanagerConfig(AppConfig):
    name = 'shiftmanager'

    def ready(self):
    	from shiftmanager import signals