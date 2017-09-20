from django.db import models
from django.conf import settings
from django.forms import ModelForm

class ShiftPlacement(models.Model):
	order = models.IntegerField(default=0)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)

class Shift(models.Model):
	DOW = (
		('Mon', 'Monday'),
		('Tue', 'Tuesday'),
		('Wed', 'Wednesday'),
		('Thur', 'Thursday'),
		('Fri', 'Friday'),
		('Sat', 'Saturday'),
		('Sun', 'Sunday'),
	)

	start = models.TimeField()
	end = models.TimeField()
	day = models.CharField(max_length=4, choices=DOW)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)

class ShiftForm(ModelForm):
	class Meta:
		model = Shift
		fields = [
			'start',
			'end',
			'day'
		]