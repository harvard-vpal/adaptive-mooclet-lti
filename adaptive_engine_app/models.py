from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Component (models.Model):
	name = models.CharField(max_length=64)

class Version (models.Model):
	component = models.ForeignKey(Component, on_delete=models.CASCADE)
	text = models.CharField(max_length=8192)

class Result (models.Model):
	student = models.CharField(max_length=64)
	version = models.ForeignKey(Version, on_delete=models.CASCADE)
	result = models.FloatField()
