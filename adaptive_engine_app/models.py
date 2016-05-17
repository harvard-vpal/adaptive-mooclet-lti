from __future__ import unicode_literals
from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.
# class Question (models.Model):
#     text = models.CharField(max_length=8192)
#     answer1 = models.CharField(max_length=1024, default="Answer1")
#     answer2 = models.CharField(max_length=1024, default="Answer2")
#     answer3 = models.CharField(max_length=1024, default="Answer3")
#     answer4 = models.CharField(max_length=1024, default="Answer4")

# class Explanation (models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer_id = models.IntegerField(default=1)
#     text = models.CharField(max_length=8192)
#     def _get_answer_text (self):
#         question = get_object_or_404(Question, id=self.question_id)
#         if self.answer_id == 1:
#             return question.answer1 
#         elif self.answer_id == 2:
#             return question.answer2
#         elif self.answer_id == 3:
#             return question.answer3
#         elif self.answer_id == 4:
#             return question.answer4
#         else:
#             raise ValueError("Invalid answer_id: {}".format(self.answer_id))
#     answer_text = property(_get_answer_text)

# class Result (models.Model):
#     student_id = models.CharField(max_length=128)
#     explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE)
#     value = models.FloatField()
#     def _get_explanation_text (self):
#         return get_object_or_404(Explanation, id=self.explanation_id).text
#     explanation_text = property(_get_explanation_text)
