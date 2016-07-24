from django import forms
from .models import *

# class SelectQualtricsForm(forms.Form):
# 	qualtrics_url = forms.CharField(label='Qualtrics URL', max_length=100)

class QuizUrlForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields = ['name','url']

class QuizForm(forms.ModelForm):
	'''
	Create new Quiz
	Used in "create_quiz" view
	'''
	use_qualtrics = forms.BooleanField(required=False)
	class Meta:
		model = Quiz
		fields = ['name']

class QuestionForm(forms.ModelForm):
	'''
	Create new Question
	Used in "create_quiz" view
	'''
	class Meta:
		model = Question
		fields = ['text']
		widgets = {
			'text': forms.Textarea(attrs={'rows':3}),
		}

class AnswerForm(forms.ModelForm):
	'''
	Create new explanation
	Used in "create_quiz" view
	'''
	class Meta:
		model = Answer
		fields = ['text', 'correct']
		widgets = {
			'text': forms.widgets.TextInput,
		}

class ExplanationForm(forms.ModelForm):
	'''
	Create new explanation
	'''
	class Meta:
		model = Explanation
		fields = ['text']
		widgets = {
			'text': forms.Textarea(attrs={'rows':3}),
		}

class ExplanationModifyForm(forms.ModelForm):
	'''
	Modify explanation
	'''
	delete = forms.BooleanField(required=False)
	class Meta:
		model = Explanation
		fields = ['text']
		widgets = {
			'text': forms.Textarea(attrs={'rows':3}),
		}

class ExplanationParameters(forms.ModelForm):
	'''
	This will be a table for each explanation, whose
	fields will be different kinds of parameters. 
	E.g. entry one might be 
	[source=inst1, role = instructor, confidence = 3, value = 0.3, weight = 5]
	'''

class SelectQuizForm(forms.Form):
	'''
	Select existing quiz for embedding
	'''
	quiz = forms.ModelChoiceField(queryset=Quiz.objects.all())

class PolicyForm(forms.ModelForm):
	'''
	Where Andrew will define the PolicyForm 
	to allow people to choose which policy to use. 
	Right now it's all thompson1
	'''
	pass

class CollaboratorForm(forms.ModelForm):
	'''
	Create Collaborator/Researcher
	'''
	class Meta:
		model = Collaborator
		fields = ['user']
		widgets = {
			'user': forms.NumberInput(),
		}

# class ValueForm(forms.ModelForm):
# 	'''
# 	enter variable value
# 	'''
# 	class Meta:
# 		model = Value
# 		fields = ['value', 'version']
# 		widgets = {
# 			'version':forms.HiddenInput(),
# 		}

class VersionValueForm(forms.ModelForm):
	'''
	Form for entering value associated with a mooclet version, and variable type
	'''
	value = forms.FloatField(label='')
	class Meta:
		model=Value
		fields = ['value']

# form class representing a row of values for a version?	
