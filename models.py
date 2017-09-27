from django.db import models
from django.conf import settings
from django.forms import ModelForm

class ShiftPlacement(models.Model):
	id = models.AutoField(primary_key=True)
	order = models.IntegerField(default=0)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)

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
	start = models.TimeField()
	end = models.TimeField()
	user = models.name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class ShiftForm(ModelForm):
	class Meta:
		model = Shift
		fields = [
			'day_of_week',
			'start',
			'end'
		]
