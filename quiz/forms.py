from django import forms
from engine.models import Answer, Value


class ChooseAnswerForm(forms.Form):
	'''
	Quiz form 1: Student chooses answer to question
	On initialization (in view), restrict the answer queryset to specific question's answer choices

	'''
	answer = forms.ModelChoiceField(
		queryset=Answer.objects.all(),
		widget=forms.RadioSelect,
		empty_label=None
	)
	

# class RateExplanationForm(forms.Form):
# 	'''
# 	Quiz form 2: Student rates the explanation they recieve
# 	Currently presents integer choices between 1 and 7
# 	'''
# 	rating = forms.ChoiceField(
# 		widget=forms.RadioSelect,
# 		choices=tuple((i,str(i)) for i in range(1,8))
# 	)
# 	explanation = forms.HiddenInput()

class RateExplanationForm(forms.ModelForm):
	'''
	Quiz form 2: Student rates the explanation they recieve
	Currently presents integer choices between 1 and 7
	'''
	# rating
	value = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=tuple((i,str(i)) for i in range(1,8))
	)
	class Meta:
		model = Value
		fields = ['value','object_id']
		widgets = {
			'object_id': forms.HiddenInput()
		}