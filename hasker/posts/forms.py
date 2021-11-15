from django import forms
from .models import Question, Answer


class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('header', 'text', 'tags')


class AnswerModelForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)