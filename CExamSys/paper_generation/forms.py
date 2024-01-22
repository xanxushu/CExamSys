from django import forms
from .models import Paper,Question
from user_management.models import CustomUser

class PaperForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Paper
        fields = ['title', 'assigned_to', 'questions']

    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
        if self.instance.pk:
            self.fields['questions'].initial = [question.pk for question in self.instance.questions.all()]
            
'''class AutoGeneratePaperForm(forms.Form):
    title = forms.CharField(label='试卷名称', max_length=200)
    question_types = forms.MultipleChoiceField(
        label='题型',
        choices=Question.TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    difficulty_from = forms.IntegerField(label='难度区间起始', min_value=1, max_value=100)
    difficulty_to = forms.IntegerField(label='难度区间结束', min_value=1, max_value=100)
    chapter = forms.MultipleChoiceField(
        label='章节选择',
        choices=[(chapter, chapter) for chapter in Question.objects.values_list('chapter', flat=True).distinct()],
        widget=forms.CheckboxSelectMultiple
    )
    num_questions = forms.IntegerField(label='每个类别题目数量', min_value=1)'''


'''class AutoGeneratePaperForm(forms.Form):
    title = forms.CharField(label='试卷名称', max_length=200)

    # 为每种题型设置题目数量
    for question_type, _ in Question.TYPE_CHOICES:
        locals()[f'num_questions_{question_type}'] = forms.IntegerField(
            label=f'{question_type}题目数量', min_value=0, required=False)

    # 为每个难度等级设置占比
    DIFFICULTY_LEVELS = (1, 2, 3, 4, 5)  # 假设有5个难度等级
    for level in DIFFICULTY_LEVELS:
        locals()[f'difficulty_{level}_percent'] = forms.IntegerField(
            label=f'难度{level}占比（%）', min_value=0, max_value=100, required=False)

    # 为每个章节设置占比
    chapter_choices = [(chapter, chapter) for chapter in Question.objects.values_list('chapter', flat=True).distinct()]
    for chapter, _ in chapter_choices:
        locals()[f'chapter_{chapter}_percent'] = forms.IntegerField(
            label=f'章节{chapter}占比（%）', min_value=0, max_value=100, required=False)

    def clean(self):
        cleaned_data = super().clean()

        # 确保至少一个题型的题目数量非零
        total_questions = sum(cleaned_data.get(f'num_questions_{question_type}', 0) for question_type, _ in Question.TYPE_CHOICES)
        if total_questions == 0:
            raise forms.ValidationError("至少为一个题型指定题目数量。")

        # 验证难度和章节占比的总和
        total_difficulty_percent = sum(cleaned_data.get(f'difficulty_{level}_percent', 0) for level in self.DIFFICULTY_LEVELS)
        total_chapter_percent = sum(cleaned_data.get(f'chapter_{chapter}_percent', 0) for chapter, _ in self.chapter_choices)
        if total_difficulty_percent != 100:
            raise forms.ValidationError("难度占比总和必须为100%。")
        if total_chapter_percent != 100:
            raise forms.ValidationError("章节占比总和必须为100%。")

        return cleaned_data
        '''
class AutoGeneratePaperForm(forms.Form):
    total_questions = forms.IntegerField(label='总题目数量', min_value=1)
    title = forms.CharField(label='试卷名称', max_length=200)
    # 为每种题型设置题目数量
    for question_type, _ in Question.TYPE_CHOICES:
        locals()[f'num_questions_{question_type}'] = forms.IntegerField(
            label=f'{question_type}题目数量', min_value=0, required=False)

    # 为每个难度设置题目数量
    DIFFICULTY_LEVELS = (1, 2, 3)  # 假设有3个难度等级
    for level in DIFFICULTY_LEVELS:
        locals()[f'num_questions_difficulty_{level}'] = forms.IntegerField(
            label=f'难度{level}题目数量', min_value=0, required=False)

    # 为每个章节设置题目数量
    chapter_choices = [(chapter, chapter) for chapter in Question.objects.values_list('chapter', flat=True).distinct()]
    for chapter, _ in chapter_choices:
        locals()[f'num_questions_chapter_{chapter}'] = forms.IntegerField(
            label=f'章节{chapter}题目数量', min_value=0, required=False)

    # 表单清理和验证总题目数量
    def clean(self):
        cleaned_data = super().clean()
        total_questions = cleaned_data.get('total_questions')

        # 检查题型数量总和
        type_total = sum(cleaned_data.get(f'num_questions_{question_type}', 0) for question_type, _ in Question.TYPE_CHOICES)
        if type_total != total_questions:
            raise forms.ValidationError("各题型题目数量总和必须等于总题目数量。")

        # 检查难度数量总和
        difficulty_total = sum(cleaned_data.get(f'num_questions_difficulty_{level}', 0) for level in self.DIFFICULTY_LEVELS)
        if difficulty_total != total_questions:
            raise forms.ValidationError("各难度题目数量总和必须等于总题目数量。")

        # 检查章节数量总和
        chapter_total = sum(cleaned_data.get(f'num_questions_chapter_{chapter}', 0) for chapter, _ in self.chapter_choices)
        if chapter_total != total_questions:
            raise forms.ValidationError("各章节题目数量总和必须等于总题目数量。")

        return cleaned_data
