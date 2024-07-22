from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Courses(models.Model):
    is_course_active = models.BooleanField(default=True, verbose_name="Курс активен")
    course_creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    course_creation_date = models.DateField(auto_now_add=True)
    course_name = models.CharField(max_length=100, name='course_name', verbose_name='Название курса')
    course_theme = models.CharField(max_length=100, name='course_theme', verbose_name='Тематика курса')
    course_description = models.TextField(name='course_description', verbose_name='Описание курса')
    course_avatar = models.ImageField(
        upload_to=f'course_avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])],
        verbose_name='Аватар Курса',
        name='course_avatar',
        default='course_avatars/istockphoto-1175435360-612x612.jpg'
    )
    course_students = models.ManyToManyField(User, blank=True, related_name='course_students',
                                             verbose_name='Ученики курса')
    objects = models.Manager()

    def __str__(self):
        return f"Курс {self.course_name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    lesson = models.IntegerField(null=True, blank=True, name='lesson', verbose_name='Номер урока в курсе')
    objects = models.Manager()

    def __str__(self):
        return f"Прогресс пользователя {self.user} в курсе {self.course} - {self.lesson}"

    class Meta:
        verbose_name = "Прогресс прохождения курса"
        verbose_name_plural = "Прогресс прохождения курсов"


class CourseFeedback(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    feedback = models.TextField(name='feedback', verbose_name='Отзыв')
    rating = models.IntegerField(name='rating', verbose_name='Рейтинг', default=0)
    objects = models.Manager()

    def __str__(self):
        return f"Отзыв пользователя {self.user} к курсу {self.course}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"