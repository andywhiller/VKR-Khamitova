# Generated by Django 5.0.3 on 2024-04-16 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_testanswer_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='testanswer',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='duration',
            field=models.IntegerField(default=1, verbose_name='Максимальная длительность ответа (в секундах)'),
        ),
    ]
