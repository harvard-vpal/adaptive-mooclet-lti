from engine.models import *
from rest_framework import serializers


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'name', 'url', 'context')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'quiz', 'text', 'url')


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Answer
		fields = ('id', 'question','text','correct')


class Explanation(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Explanation
		fields = ('id', 'answer','text')


class ResultSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Result
		fields = ('id', 'user','explanation','value')