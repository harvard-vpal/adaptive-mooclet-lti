from django import forms
from engine.models import Answer


class ChooseAnswerForm(forms.Form):
	'''
	Quiz form 1: Student chooses answer to question
	On initialization (in view), restrict the answer queryset to specific question's answer choices

	'''
	answer = forms.ModelChoiceField(queryset=Answer.objects.all(),widget=forms.RadioSelect,empty_label=None)
	

class RateExplanationForm(forms.Form):
	'''
	Quiz form 2: Student rates the explanation they recieve
	Currently presents integer choices between 1 and 7
	'''
	rating = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=tuple((i,str(i)) for i in range(1,8))
	)

