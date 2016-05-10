from django.contrib import admin

# Register your models here.
from .models import Question, Explanation, Result

class ExplanationAdmin (admin.ModelAdmin):
	list_display = ('answer_text', 'text')

class ResultAdmin (admin.ModelAdmin):
	list_display = ('explanation_text', 'student', 'value')

admin.site.register(Question)
admin.site.register(Explanation, ExplanationAdmin)
admin.site.register(Result, ResultAdmin)
