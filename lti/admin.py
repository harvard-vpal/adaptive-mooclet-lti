from django.contrib import admin

# Register your models here.
from .models import Quiz, Question, Answer, Explanation, Result

class QuizAdmin (admin.ModelAdmin):
	list_display = ['name','user','url','course']

class QuestionAdmin (admin.ModelAdmin):
	list_display = ['quiz','text']

class AnswerAdmin (admin.ModelAdmin):
	# list_display = Answer._meta.get_all_field_names()
	list_display = ['question','text','order','correct']

class ExplanationAdmin (admin.ModelAdmin):
	list_display = ['answer','text']

class ResultAdmin (admin.ModelAdmin):
	list_display = ['student','explanation','value']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Explanation, ExplanationAdmin)
admin.site.register(Result, ResultAdmin)
