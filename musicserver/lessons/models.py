from django.db import models
from django.contrib.auth.models import User
from course.models import Courses
from django_ckeditor_5.fields import CKEditor5Field



class Lesson(models.Model):
    is_lesson_active = models.BooleanField(default=True)
    lesson_creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    lesson_creation_date = models.DateField(auto_now_add=True)
    lesson_name = models.CharField(max_length=100, name='lesson_name', verbose_name='Название урока')
    lesson_theme = models.CharField(max_length=100, name='lesson_theme', verbose_name='Тематика урока')
    lesson_description = models.TextField(name='lesson_description', verbose_name='Описание урока')
    lesson_course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    lesson_content = CKEditor5Field(name='lesson_content', verbose_name='Содержание урока', blank=True)
    lesson_students = models.ManyToManyField(User, blank=True, related_name='lesson_students',
                                             verbose_name='Ученики урока')
    lesson_priority = models.IntegerField(null=True, blank=True, name='lesson_priority', verbose_name='Приоритет урока')
    test = models.ForeignKey('tests.Test', null=True, blank=True, on_delete=models.SET_NULL)
    objects = models.Manager()

    def __str__(self):
        return f"Урок {self.lesson_name} в курсе {self.lesson_course}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

