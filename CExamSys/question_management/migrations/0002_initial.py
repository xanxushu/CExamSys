# Generated by Django 4.2 on 2023-12-20 05:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='assigned_to',
            field=models.ManyToManyField(related_name='assigned_questions', to=settings.AUTH_USER_MODEL),
        ),
    ]
