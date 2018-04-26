from django import forms
from . models import ShiftFile

class ShiftExcelUpload(forms.Form):
	title = forms.CharField(max_length=50)
	sheet = forms.FileField()

	class Meta:
		model = ShiftFile
		fields = [
			"title",
			"sheet"
		]
