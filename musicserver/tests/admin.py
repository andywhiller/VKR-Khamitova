from django.contrib import admin
from . import models

admin.site.register(models.Test)
admin.site.register(models.TestQuestion)
admin.site.register(models.TestAnswer)
admin.site.register(models.NoteSet)
admin.site.register(models.TestAnswerVariant)

