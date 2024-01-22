# Generated by Django 4.2 on 2023-12-24 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paper_generation', '0001_initial'),
        ('question_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_management.question'),
        ),
    ]