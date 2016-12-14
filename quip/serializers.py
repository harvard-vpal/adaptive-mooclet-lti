from rest_framework import serializers
from .models import *

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['name','user','url','course']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['name','quiz','text','url']
