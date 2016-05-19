from django import forms
from .models import Quiz, Question, Answer, Explanation

# class SelectQualtricsForm(forms.Form):
# 	qualtrics_url = forms.CharField(label='Qualtrics URL', max_length=100)

class QualtricsQuizForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields = ['name','url']

class QuizForm(forms.ModelForm):
	'''
	Create new Quiz
	Used in "create_quiz" view
	'''
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

class AnswerForm(forms.ModelForm):
	'''
	Create new explanation
	Used in "create_quiz" view
	'''
	class Meta:
		model = Answer
		fields = ['text', 'correct', 'order']


class ExplanationForm(forms.ModelForm):
	'''
	Create new explanation
	Used in "create_quiz" view
	'''
	class Meta:
		model = Explanation
		fields = ['text']

class SelectQuizForm(forms.Form):
	'''
	Select existing quiz for embedding
	'''
	quiz = forms.ModelChoiceField(queryset=Quiz.objects.all())


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

