from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import os

from . scrape import scrape_schedule
from . models import ShiftFile

@receiver(post_save, sender=ShiftFile)
def scrape_new_sheet(sender, instance, created, **kwargs):
	if created:
		sheet_path = os.path.join(settings.BASE_DIR, instance.sheet.name)
		shifts = scrape_schedule(sheet_path)
		for shift in shifts:
			print(shift)

#register signals
post_save.connect(scrape_new_sheet, sender=ShiftFile)