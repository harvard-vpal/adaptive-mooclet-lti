from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Component (models.Model):
	component_name = models.CharField(max_length=64)

class Version (models.Model):
	component = models.ForeignKey(Component, on_delete=models.CASCADE)
	text = models.CharField(max_length=8192)

class Student (models.Model):
	student_id = models.CharField(max_length=64, primary_key=True)  # From LTI

class Result (models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	version = models.ForeignKey(Version, on_delete=models.CASCADE)
	result = models.FloatField()
