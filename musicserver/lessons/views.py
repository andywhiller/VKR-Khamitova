from django.shortcuts import render, redirect
from django.views import View
from . import forms
from .models import Lesson
from course.models import Courses, CourseProgress
from tests.models import Test, TestAnswer, TestQuestion
from tests.forms import OneAnswerTest, ManyAnswerTest, FileAnswerTest, NoteAnswerForm, OpenAnswerTest
from musicserver.settings import MEDIA_URL


# представление создания урока
class AddLessonView(View):
    def get(self, request, pk):
        course = Courses.objects.get(id=pk)
        form = forms.AddLessonForm()
        tests = Test.objects.filter(test_creator=request.user)
        return render(request, 'main/add_lesson.html', {'form': form, 'action': 'Добавление',
                                                        'button_text': "Добавить", 'tests': tests, 'course': course})

    def post(self, request, pk):
        form = forms.AddLessonForm(request.POST, request.FILES)
        course = Courses.objects.get(id=pk)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.lesson_course = course
            lesson.lesson_creator = request.user
            lesson.save()
            return redirect('current_course', pk=course.id)
        return render(request, 'main/add_lesson.html', {'form': form, 'action': 'Добавление',
                                                        'button_text': "Добавить", 'course': course})


# представление просмотра урока
class LessonView(View):
    def get(self, request, pk):
        lesson = Lesson.objects.get(id=pk)
        try:
            test = lesson.test
            test_forms = []
            answers_render = []
            answers = TestAnswer.objects.filter(user=request.user, question__test=test)
            answered_questions = TestQuestion.objects.filter(test=test, id__in=answers.values('question'))
            remained_questions = test.questions.all().difference(answered_questions)
            print(answered_questions, remained_questions)
            for question in remained_questions:
                if question.type == 'one':
                    f = OneAnswerTest()
                    f.fields['question'].initial = question.id
                    f.fields['answer'].widget.choices = [(answer.answer, answer.answer) for answer in question.answers.all()]
                    test_forms.append(f)
                elif question.type == 'many':
                    f = ManyAnswerTest()
                    f.fields['question'].initial = question.id
                    f.fields['answer'].widget.choices = [(answer.answer, answer.answer) for answer in question.answers.all()]
                    test_forms.append(f)
                elif question.type == 'open':
                    f = OpenAnswerTest()
                    f.fields['question'].initial = question.id
                    test_forms.append(f)
                elif question.type == 'file':
                    f = FileAnswerTest()
                    f.fields['question'].initial = question.id
                    test_forms.append(f)
                elif question.type == 'note':
                    f = NoteAnswerForm()
                    f.fields['question'].initial = question.id
                    test_forms.append(f)
            if len(remained_questions) == 0:
                for answer in answers:
                    answers_render.append([
                        answer.answer.strip('[]').replace("'", '') if answer.question.type != 'file' else f'<a href="{MEDIA_URL}{answer.media}">ссылка</a>',
                        answer.question.question, ", ".join([a for a in answer.question.correct_answer.all().values_list('answer', flat=True)]),
                        answer.score,
                        answer.question.score,
                        answer.comment])
            return render(request, 'main/lesson.html',
                          {'lesson': lesson, 'test_forms': test_forms, 'test': zip(test_forms, remained_questions), 'answers_render': answers_render})
        except AttributeError:
            return render(request, 'main/lesson.html',
                          {'lesson': lesson, 'test_forms': [], 'test': zip([], [])})

    def post(self, request, pk):
        lesson = Lesson.objects.get(id=pk)
        progress = CourseProgress.objects.get(course=lesson.lesson_course, user=request.user)
        progress.lesson = lesson.lesson_priority
        progress.save()
        return redirect('current_course', pk=lesson.lesson_course.id)


# представление изменения урока
class UpdateLessonView(View):
    def get(self, request, pk):
        lesson = Lesson.objects.get(id=pk)
        form = forms.AddLessonForm(instance=lesson)
        tests = Test.objects.filter(test_creator=request.user)
        return render(request, 'main/add_lesson.html', {'form': form, 'action': 'Изменение',
                                                        'button_text': "Сохранить", 'tests': tests, 'course': lesson.lesson_course, 'lesson': lesson})

    def post(self, request, pk):
        lesson = Lesson.objects.get(id=pk)
        form = forms.AddLessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('current_course', pk=lesson.lesson_course.id)
        return render(request, 'main/add_lesson.html', {'form': form, 'action': 'Изменение',
                                                        'button_text': "Сохранить", 'course': lesson.lesson_course, 'lesson': lesson})


# представление удаления урока
class DeleteLessonView(View):
    def get(self, request, pk):
        lesson = Lesson.objects.get(id=pk)
        lesson.delete()
        return redirect('current_course', pk=lesson.lesson_course.id)

