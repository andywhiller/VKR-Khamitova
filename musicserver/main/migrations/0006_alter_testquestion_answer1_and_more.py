# Generated by Django 5.0.3 on 2024-04-14 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_test_testquestion_lesson_test_testanswer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestion',
            name='answer1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ответ 1'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='answer2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ответ 2'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='answer3',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ответ 3'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='answer4',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ответ 4'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='answer5',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ответ 5'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='answer6',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ответ 6'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='answer7',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ответ 7'),
        ),
    ]