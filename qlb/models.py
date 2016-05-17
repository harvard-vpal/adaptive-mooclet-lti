from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Instructor(models.Model):
#     user = models.OneToOneField(User, 
#     	# on_delete=models.CASCADE
#     	)
    

class Quiz(models.Model):
    name = models.CharField('quiz name', max_length=100)
    user = models.ForeignKey(User)
    url = models.CharField(max_length=200)
    course = models.PositiveIntegerField()
    def __unicode__(self):
    	return self.name


    # resource_location = None

class Question(models.Model):
	quiz = models.ForeignKey(Quiz)
	text = models.CharField('question text', max_length=500)

class Answer(models.Model):
	question = models.ForeignKey(Question)
	text = models.CharField('answer choice text', max_length=500)
	order = models.PositiveIntegerField('choice order')
	correct = models.BooleanField('is correct')

class Explanation(models.Model):
	answer = models.ForeignKey(Answer)
	text = models.CharField('explanation text', max_length=500)
