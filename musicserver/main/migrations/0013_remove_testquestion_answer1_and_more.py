# Generated by Django 5.0.3 on 2024-04-28 06:50

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_courses_course_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testquestion',
            name='answer1',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='answer2',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='answer3',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='answer4',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='answer5',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='answer6',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='answer7',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_content',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Содержание урока'),
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='correct_answer',
        ),
        migrations.CreateModel(
            name='TestAnswerVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.testquestion')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответов',
            },
        ),
        migrations.AddField(
            model_name='testquestion',
            name='answers',
            field=models.ManyToManyField(blank=True, related_name='answers', to='main.testanswervariant', verbose_name='Варианты ответов'),
        ),
        migrations.AddField(
            model_name='testquestion',
            name='correct_answer',
            field=models.ManyToManyField(blank=True, null=True, related_name='correct_answer', to='main.testanswervariant', verbose_name='Правильные ответы'),
        ),
    ]