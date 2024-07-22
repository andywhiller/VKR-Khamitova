from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

from course.models import Courses


class Userdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fathersname = models.CharField(max_length=50, null=True, blank=True, name='fathersname', verbose_name='Отчество')
    birthdate = models.DateField(null=True, blank=True, name='birthdate', verbose_name='Дата рождения')
    musicedu = models.CharField(max_length=50, null=True, blank=True, name='musicedu',
                                verbose_name='Музыкальное образование')
    phone = models.IntegerField(null=True, blank=True, name='phone', verbose_name='Номер телефона')
    profile_avatar = models.ImageField(
        upload_to=f'profile_avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])],
        verbose_name='Аватар профиля',
        name='profile_avatar'
    )
    objects = models.Manager()

    def __str__(self):
        return f"Пользователь {self.user}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"




