from django import forms
from . import models


class AllCoursesForm(forms.ModelForm):
    class Meta:
        model = models.Courses
        fields = ['course_name', 'course_theme', 'course_description', 'course_avatar']


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = models.Courses
        fields = ['is_course_active', 'course_name', 'course_theme', 'course_description', 'course_avatar']


class AddFeedbackForm(forms.ModelForm):
    class Meta:
        model = models.CourseFeedback
        fields = ['feedback', 'rating']