from django import forms
from . models import ShiftFile
from django.utils.translation import ugettext_lazy as _

class ShiftExcelUpload(forms.ModelForm):

	def is_valid(self):
		valid = super(ShiftExcelUpload, self).is_valid()

		if not valid:
			return valid

		#If the last 5 characters aren't .xlsm..
		if self.cleaned_data['sheet'].name[-5:] != ".xlsm":
			return forms.ValidationError(_("Please only upload .xlsm files."), code='filetype', params={})

		return True

	class Meta:
		model = ShiftFile
		fields = [
			"sheet",
			"first_date",
			"last_date"
		]
