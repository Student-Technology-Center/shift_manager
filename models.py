from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.utils import timezone

import django

class Shift(models.Model):
	DOW = (
		('Mon', 'Monday'),
		('Tue', 'Tuesday'),
		('Wed', 'Wednesday'),
		('Thu', 'Thursday'),
		('Fri', 'Friday'),
		('Sat', 'Saturday'),
		('Sun', 'Sunday')
	)

	day_of_week = models.CharField(max_length=3, choices=DOW)
	date 		= models.DateField(null=True)
	start 		= models.TimeField()
	sheet_user 	= models.CharField(max_length=64, null=False)
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

class ShiftFile(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
	created_at 	= models.DateTimeField(auto_now_add=True)
	first_date 	= models.DateField(null=False, default=django.utils.timezone.now)
	last_date 	= models.DateField(null=False, default=django.utils.timezone.now)
	sheet 		= models.FileField(upload_to='media/sheets/%Y-%m-%d/')

	def filename(self):
	    return os.path.basename(self.sheet.name)
