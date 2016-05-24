from django.contrib import admin

# Register your models here.
from .models import *

class TemplateAdmin (admin.ModelAdmin):
	pass


admin.site.register(Template, TemplateAdmin)
