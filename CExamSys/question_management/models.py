from django.db import models
from django.conf import settings

class Question(models.Model):
    TYPE_CHOICES = (
        ('SZ', '选择题'),
        ('TK', '填空题'),
        ('PD', '判断题'),
        ('SF', '简答题')
        # 可以根据需要添加更多题型
    )

    question_text = models.TextField()
    answer = models.TextField()
    difficulty = models.IntegerField()
    question_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    chapter = models.CharField(max_length=100)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_questions')

    def __str__(self):
        return self.question_text
