from django import forms
from . models import ShiftFile

class ShiftExcelUpload(forms.ModelForm):
	class Meta:
		model = ShiftFile
		fields = [
			"sheet"
		]
