# Generated by Django 5.0.3 on 2024-04-06 07:15

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courses',
            options={'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'Урок', 'verbose_name_plural': 'Уроки'},
        ),
        migrations.AlterModelOptions(
            name='userdata',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='courses',
            name='is_course_active',
            field=models.BooleanField(default=True, verbose_name='Курс активен'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_content',
            field=ckeditor.fields.RichTextField(verbose_name='Содержание урока'),
        ),
    ]
