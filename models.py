from django.db import models
from django.conf import settings

class ShiftPlacement(models.Model):
	order = models.IntegerField(primary_key=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
