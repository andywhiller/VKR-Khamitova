from django.contrib import admin
from . import models


@admin.register(models.Userdata)
class UserdataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fathersname', 'birthdate', 'musicedu', 'phone', 'profile_avatar')
    list_display_links = ('id', 'user')
