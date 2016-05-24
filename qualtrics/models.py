from django.db  import models

class Template(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)

	# if this is not blank, signifies that we have a local QSF file
	filename = models.CharField(max_length=200, default='')

	def __unicode__(self):
		return self.name