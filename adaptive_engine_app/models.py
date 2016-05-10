from __future__ import unicode_literals
from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.
class Course (models.Model):
	course_name = models.CharField(max_length=128)
	instructor_name = models.CharField(max_length=128)
	instructor_email = models.CharField(max_length=128)

class Quiz (models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Question (models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	text = models.CharField(max_length=8192)

class Answer (models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=8192)
	def _get_question_text (self):
		return get_object_or_404(Question, id=self.question_id).text
	question_text = property(_get_question_text)

class Explanation (models.Model):
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	text = models.CharField(max_length=8192)
	def _get_answer_text (self):
		return get_object_or_404(Answer, id=self.answer_id).text
	answer_text = property(_get_answer_text)

class Result (models.Model):
	student = models.CharField(max_length=128)
	explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE)
	value = models.FloatField()
	def _get_explanation_text (self):
		return get_object_or_404(Explanation, id=self.explanation_id).text
	explanation_text = property(_get_explanation_text)
