from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'answer', 'difficulty', 'question_type', 'chapter', 'assigned_to']

class QuestionSearchForm(forms.Form):
    qid = forms.IntegerField(required=False, label='题目ID')
    keyword = forms.CharField(required=False, label='关键词')
    question_type_choices = [('', '---------')] + list(Question.TYPE_CHOICES)
    question_type = forms.ChoiceField(choices=question_type_choices, required=False, label='题型')
    chapter = forms.CharField(required=False, label='章节')
    difficulty_from = forms.IntegerField(required=False, label='难度（最小）')
    difficulty_to = forms.IntegerField(required=False, label='难度（最大）')

