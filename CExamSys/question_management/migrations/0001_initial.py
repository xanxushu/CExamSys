# Generated by Django 4.2 on 2023-12-24 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('answer', models.TextField()),
                ('difficulty', models.IntegerField()),
                ('question_type', models.CharField(choices=[('XZ', '选择题'), ('TK', '填空题'), ('PD', '判断题'), ('SF', '简答题')], max_length=2)),
                ('chapter', models.CharField(max_length=100)),
            ],
        ),
    ]