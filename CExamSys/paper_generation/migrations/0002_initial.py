# Generated by Django 4.2 on 2023-12-20 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paper_generation', '0001_initial'),
        ('question_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='questions',
            field=models.ManyToManyField(to='question_management.question'),
        ),
    ]
