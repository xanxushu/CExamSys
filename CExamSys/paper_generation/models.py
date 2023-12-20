from django.db import models
from question_management.models import Question

class Paper(models.Model):
    questions = models.ManyToManyField(Question)
    total_questions = models.IntegerField()
    paper_answer = models.TextField()
    difficulty_ratio = models.CharField(max_length=100)  # 例如 "50% Easy, 30% Medium, 20% Hard"
    chapter_ratio = models.CharField(max_length=100)  # 例如 "Chapter 1: 30%, Chapter 2: 70%"

    def __str__(self):
        return f"Paper {self.id} with {self.total_questions} questions"
