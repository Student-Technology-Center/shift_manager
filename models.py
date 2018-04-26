from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.utils import timezone

import django

class ShiftHelper(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', null=True)
	current_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	current_place = models.IntegerField(default=0)
	max_place = models.IntegerField(default=0)
	start_date = models.DateField(default=django.utils.timezone.now)
	end_date = models.DateField(default=django.utils.timezone.now)
	current_round = models.IntegerField(default=0)
	total_rounds = models.IntegerField(default=3)
	going_up = models.BooleanField(default=True)
	shifts_per_turn = models.IntegerField(default=4)

class ShiftPlacement(models.Model):
	place = models.IntegerField(default=0)
	amt_left = models.IntegerField(default=4)
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
	date = models.DateField(null=True)
	start = models.TimeField()
	end = models.TimeField()
	up_for_grabs = models.BooleanField(default=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ShiftFile(models.Model):
	sheet = models.FileField(upload_to='sheets/%Y-%m-%d/')
