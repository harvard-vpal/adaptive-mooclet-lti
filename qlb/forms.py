from django import forms

class SelectQualtricsForm(forms.Form):
	qualtrics_url = forms.CharField(label='Qualtrics URL', max_length=100)