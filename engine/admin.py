from django.contrib import admin

# Register your models here.
from .models import *

class QuizAdmin (admin.ModelAdmin):
	list_display = ['id','name','user']

class QuestionAdmin (admin.ModelAdmin):
	list_display = ['id','get_quiz_id','quiz','text']

	def get_quiz_id(self,obj):
		return obj.quiz.id

class AnswerAdmin (admin.ModelAdmin):
	list_display = ['id','question','text','correct']

class ExplanationAdmin (admin.ModelAdmin):
	list_display = ['id','answer','text']

class ResultAdmin (admin.ModelAdmin):
	list_display = ['id','user','explanation','value']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Explanation, ExplanationAdmin)
admin.site.register(Result, ResultAdmin)
