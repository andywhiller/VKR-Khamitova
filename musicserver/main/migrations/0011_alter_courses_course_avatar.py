# Generated by Django 5.0.3 on 2024-04-25 06:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_noteset_alter_lesson_lesson_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='course_avatar',
            field=models.ImageField(blank=True, default='course_avatars/photo_2024-04-24_21-29-27.jpg', null=True, upload_to='course_avatars/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])], verbose_name='Аватар Курса'),
        ),
    ]
