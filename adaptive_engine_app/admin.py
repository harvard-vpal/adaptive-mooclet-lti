from django.contrib import admin

# Register your models here.
from .models import Course, Quiz, Question, Answer, Explanation, Result

class AnswerAdmin (admin.ModelAdmin):
	list_display = ('question_text', 'text')

class ExplanationAdmin (admin.ModelAdmin):
	list_display = ('answer_text', 'text')

class ResultAdmin (admin.ModelAdmin):
	list_display = ('explanation_text', 'student', 'value')

admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Explanation, ExplanationAdmin)
admin.site.register(Result, ResultAdmin)
