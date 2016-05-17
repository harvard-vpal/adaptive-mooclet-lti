from django import forms
from .models import Quiz, Question, Answer, Explanation

class SelectQualtricsForm(forms.Form):
	qualtrics_url = forms.CharField(label='Qualtrics URL', max_length=100)

class CreateQuizForm(forms.Form):
	name = forms.CharField(label='name',max_length=100)
	question = forms.CharField(label='question',max_length=100)
	answer1 = forms.CharField(label='answer 1',max_length=100)
	answer2 = forms.CharField(label='answer 2',max_length=100)
	explanation1a = forms.CharField(label='answer 1 explanation 1',max_length=100)
	explanation1b = forms.CharField(label='answer 1 explanation 2',max_length=100)
	explanation2a = forms.CharField(label='answer 2 explanation 1',max_length=100)
	explanation2b = forms.CharField(label='answer 2 explanation 2',max_length=100)

class QuizForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields = ['name']

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['text']

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['text', 'order', 'correct']


class ExplanationForm(forms.ModelForm):
	class Meta:
		model = Explanation
		fields = ['text']

class SelectQuizForm(forms.Form):
	quiz = forms.ModelChoiceField(queryset=Quiz.objects.all())

