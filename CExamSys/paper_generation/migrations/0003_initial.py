# Generated by Django 4.2 on 2023-12-24 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('question_management', '0001_initial'),
        ('paper_generation', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='assigned_to',
            field=models.ManyToManyField(related_name='assigned_papers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paper',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_papers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paper',
            name='questions',
            field=models.ManyToManyField(through='paper_generation.PaperQuestion', to='question_management.question'),
        ),
    ]
