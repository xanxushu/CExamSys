from django.db import models
from django.conf import settings
from question_management.models import Question  # 确保导入Question模型

class Paper(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_papers')
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_papers')
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(Question, through='PaperQuestion')

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def difficulty(self):
        total_difficulty = sum(question.difficulty for question in self.questions.all())
        return total_difficulty / self.question_count if self.question_count > 0 else 0

    @property
    def chapter_distribution(self):
        distribution = {}
        for question in self.questions.all():
            distribution[question.chapter] = distribution.get(question.chapter, 0) + 1
        return distribution

    def __str__(self):
        return self.title

class PaperQuestion(models.Model):
    paper = models.ForeignKey(Paper, related_name='paper_questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.paper.title} - {self.question.question_text}"
