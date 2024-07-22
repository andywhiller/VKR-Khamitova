from django.db import models
from django.contrib.auth.models import User

class TestQuestion(models.Model):
    question_short = models.CharField(max_length=100, name='question_short', verbose_name='Вопрос')
    question = models.TextField(name='question', verbose_name='Вопрос')
    media = models.FileField(upload_to=f'test_media/', null=True, blank=True, verbose_name='Медиа', name='media')
    type = models.CharField(max_length=100, name='type', verbose_name='Тип вопроса',
                            choices=(('one', 'Один правильный ответ'),
                                     ('many', 'Несколько правильных ответов'),
                                     ('open', 'Развёрнутый ответ'),
                                     ('file', 'Ответ-файл'),
                                     ('note', 'Ноты')), default='one')
    num_answers = models.IntegerField(name='num_answers', verbose_name='Количество ответов', default=1)
    answers = models.ManyToManyField('TestAnswerVariant', blank=True, verbose_name='Варианты ответов', related_name='answers')
    correct_answer = models.ManyToManyField('TestAnswerVariant', blank=True, null=True, verbose_name='Правильные ответы', related_name='correct_answer')
    duration = models.IntegerField(name='duration', verbose_name='Максимальная длительность ответа (в секундах)',
                                   default=1)
    score = models.IntegerField(name='score', verbose_name='Баллы за задание')
    objects = models.Manager()

    def __str__(self):
        return f"Вопрос {self.question_short}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class TestAnswerVariant(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, name='answer', verbose_name='Ответ', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"Вариант ответа {self.answer} к вопросу {self.question}"

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"


class TestAnswer(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, name='answer', verbose_name='Ответ')
    score = models.IntegerField(name='score', verbose_name='Баллы за ответ', default=0)
    media = models.FileField(upload_to=f'answer_media/', null=True, blank=True, verbose_name='Медиа', name='media')
    checked = models.BooleanField(name='checked', verbose_name='Проверен', default=False)
    comment = models.TextField(name='comment', verbose_name='Комментарий', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"Ответ {self.answer} к вопросу {self.question}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Test(models.Model):
    name = models.CharField(max_length=100, name='name', verbose_name='Название теста')
    test_creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='tests')
    questions = models.ManyToManyField(TestQuestion)
    objects = models.Manager()

    def __str__(self):
        return f"Тест {self.name}"

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class NoteSet(models.Model):
    name = models.CharField(max_length=100, name='name', verbose_name='Название нот')
    notes = models.TextField(name='notes', verbose_name='Ноты (json)', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"Ноты {self.name}"

    class Meta:
        verbose_name = "Ноты"
        verbose_name_plural = "Ноты"
        