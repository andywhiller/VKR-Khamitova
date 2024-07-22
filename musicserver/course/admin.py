from django.contrib import admin
from . import models

admin.site.register(models.Courses)
admin.site.register(models.CourseProgress)
admin.site.register(models.CourseFeedback)
