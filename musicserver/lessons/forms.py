from django import forms
from . import models

class AddLessonForm(forms.ModelForm):
    class Meta:
        model = models.Lesson
        exclude = ['lesson_creator', 'lesson_creation_date', 'lesson_students', 'lesson_course']
