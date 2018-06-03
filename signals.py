from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import os

from . helpers import scrape_schedule, create_shifts
from . models import ShiftFile, Shift

@receiver(post_save, sender=ShiftFile)
def scrape_new_sheet(sender, instance, created, **kwargs):
	if created:

		#Delete to make room for new shifts.
		for shift in Shift.objects.all():
			shift.delete()

		#Scrape the sheets and get a list of shifts
		shifts = scrape_schedule(instance.sheet.path)

		#Finally, attempt to attach the shifts to a user.
		create_shifts(shifts, instance)

#register signals
post_save.connect(scrape_new_sheet, sender=ShiftFile)