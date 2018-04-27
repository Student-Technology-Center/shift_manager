from django.db.models.signals import post_save
from django.dispatch import receiver

from . models import ShiftFile

@receiver(post_save, sender=ShiftFile)
def scrape_new_sheet(sender, instance, created, **kwargs):
	if created:
		print("Created a new sheet!")

#register signals
post_save.connect(scrape_new_sheet, sender=ShiftFile)