from django.shortcuts import render
from django.views import View
from .models import Test, NoteSet, TestQuestion, TestAnswer, TestAnswerVariant
from . import forms
from django.http import JsonResponse
from django.shortcuts import redirect
import ast
from lessons.models import Lesson


# представление нотного редактора
class NotesEditor(View):
    def get(self, request):
        return render(request, 'main/notes_editor.html')

    def post(self, request):
        note = NoteSet()
        note.notes = request.POST.get('notes')
        note.name = request.POST.get('name')
        print(note.notes)
        note.save()
        return JsonResponse({'id': note.id})


# представление создания теста
class AddTestView(View):
    def get(self, request):
        form = forms.AddTestForm()
        return render(request, 'main/add_test.html', {'form': form})

    def post(self, request):
        form = forms.AddTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.test_creator = request.user
            test.save()
            return redirect('view_test', pk=form.instance.id)
        return render(request, 'main/add_test.html', {'form': form})


# представление изменения теста
class EditTestView(View):
    def get(self, request, pk):
        test = Test.objects.get(pk=pk)
        form = forms.AddTestForm(instance=test)
        return render(request, 'test_form.html', {'form': form})

    def post(self, request, pk):
        test = Test.objects.get(pk=pk)
        form = forms.AddTestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('view_lesson', pk=test.lesson_set.first().id)
        return render(request, 'test_form.html', {'form': form})


# представление обработчика тестирования
class TestProcessor(View):
    def post(self, request, *args, **kwargs):
        # обработчик тестирования для вопросов с одним правильным вариантом ответа
        if kwargs['type'] == 'one':
            f = forms.OneAnswerTest(request.POST)
            if f.is_valid():
                print(f.cleaned_data)
                question = TestQuestion.objects.get(id=f.cleaned_data['question'])
                answer = TestAnswer()
                answer.question = question
                answer.user = request.user
                answer.answer = f.cleaned_data['answer']
                answer.checked = True
                if f.cleaned_data['answer'] == question.correct_answer.first().answer:
                    answer.score = question.score
                answer.save()
                return redirect('view_lesson', pk=kwargs['lesson'])
            else:
                print(f.errors)
                return redirect('view_lesson', pk=kwargs['lesson'])
        # обработчик тестирования для вопросов с несколькими правильными вариантами ответа
        elif kwargs['type'] == 'many':
            f = forms.ManyAnswerTest(request.POST)
            if f.is_valid():
                question = TestQuestion.objects.get(id=f.cleaned_data['question'])
                answer = TestAnswer()
                answer.question = question
                answer.user = request.user
                answer.answer = f.cleaned_data['answer']
                answer.checked = True
                form_answers = ast.literal_eval(f.cleaned_data['answer'])
                question_answers = question.correct_answer.all().values_list('answer', flat=True)
                if len(set(form_answers).intersection(question_answers)) == len(question_answers):
                    answer.score = question.score
                answer.save()
                return redirect('view_lesson', pk=kwargs['lesson'])
            else:
                print(f.errors)
                return redirect('view_lesson', pk=kwargs['lesson'])
        # обработчик тестирования для вопросов с открытым ответом
        elif kwargs['type'] == 'open':
            f = forms.OpenAnswerTest(request.POST)
            if f.is_valid():
                question = TestQuestion.objects.get(id=f.cleaned_data['question'])
                answer = TestAnswer()
                answer.question = question
                answer.user = request.user
                answer.answer = f.cleaned_data['answer']
                answer.save()
                return redirect('view_lesson', pk=kwargs['lesson'])
            else:
                print(f.errors)
                return redirect('view_lesson', pk=kwargs['lesson'])
        # обработчик тестирования для вопросов, в ответ на которые требуется прикрепить файл
        elif kwargs['type'] == 'file':
            f = forms.FileAnswerTest(request.POST, request.FILES)
            if f.is_valid():
                question = TestQuestion.objects.get(id=f.cleaned_data['question'])
                answer = TestAnswer()
                answer.question = question
                answer.user = request.user
                answer.media = f.cleaned_data['answer']
                answer.answer = f.cleaned_data['comment']
                answer.save()
                return redirect('view_lesson', pk=kwargs['lesson'])
            else:
                print(f.errors)
                return redirect('view_lesson', pk=kwargs['lesson'])
        # обработчик тестирования для вопросов, ответ на которые заключаются в нотах
        elif kwargs['type'] == 'note':
            f = forms.NoteAnswerForm(request.POST)
            if f.is_valid():
                question = TestQuestion.objects.get(id=f.cleaned_data['question'])
                answer = TestAnswer()
                answer.question = question
                answer.user = request.user
                answer.answer = f.cleaned_data['answer']
                answer.comment = f.cleaned_data['comment']
                answer.save()
                return redirect('view_lesson', pk=kwargs['lesson'])
            else:
                print(f.errors)
                return redirect('view_lesson', pk=kwargs['lesson'])


# представление отображения списка тестирований пользователя (прогресса)
class UserTests(View):
    def get(self, request, *args, **kwargs):
        tests = TestAnswer.objects.filter(user=request.user)
        user_tests = []
        for test in tests:
            q = test.question
            t = Test.objects.get(questions__in=[q])
            print(t.lesson_set.first().lesson_name)
            user_tests.append(t)
        user_tests = list(set(user_tests))
        checked = []
        res = []
        maxs = []
        for test in user_tests:
            value = True
            score = 0
            maxsc = 0
            for question in test.questions.all():
                answer = TestAnswer.objects.get(user=request.user, question=question)
                maxsc += question.score
                if not answer.checked:
                    value = False
                else:
                    score += answer.score
            checked.append(value)
            res.append(score)
            maxs.append(maxsc)
        return render(request, 'main/all_tests.html',
                      {'tests': zip(user_tests, checked, res, maxs), 'user_tests': user_tests})


# представление просмотра теста
class TestView(View):
    def get(self, request, pk):
        test = Test.objects.get(pk=pk)
        for q in test.questions.all():
            for a in TestAnswerVariant.objects.filter(question=q):
                if a not in q.answers.all():
                    a.delete()
        form = forms.AddTestQuestionForm()
        return render(request, 'main/test.html', {'test': test, 'form': form})

    def post(self, request, pk):
        test = Test.objects.get(pk=pk)
        form = forms.AddTestQuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            for var in TestAnswerVariant.objects.filter(question_id=100015):
                var.question = question
                var.save()
                question.answers.add(var)
            test.questions.add(question)
            test.save()
            return redirect('view_test', pk=pk)
        return render(request, 'main/test.html', {'test': test, 'form': form})


# представление удаления вопроса теста
class DeleteQuestion(View):
    def get(self, request, pk):
        question = TestQuestion.objects.get(pk=pk)
        test = question.test_set.first().id
        question.delete()
        return redirect('view_test', pk=test)


# представление изменения вопроса теста
class UpdateQuestion(View):
    def get(self, request, pk):
        question = TestQuestion.objects.get(pk=pk)
        test = question.test_set.first()
        form = forms.AddTestQuestionForm(instance=question)
        return render(request, 'main/test.html', {'form': form, 'question': question, 'test': test, 'expanded': True})

    def post(self, request, pk):
        question = TestQuestion.objects.get(pk=pk)
        test = question.test_set.first()
        form = forms.AddTestQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            for var in TestAnswerVariant.objects.filter(question_id=question.id):
                var.question = question
                var.save()
                question.answers.add(var)
            test.questions.add(question)
            test.save()
            return redirect('view_test', pk=question.test_set.first().id)
        return render(request, 'main/test.html', {'form': form, 'question': question, 'test': test, 'expanded': True})


# представление отображения списка ответов учеников на проверку преподавателю
class TestChecker(View):
    def get(self, request):
        lessons = Lesson.objects.filter(lesson_creator=request.user)
        tests = [l.test for l in lessons if l.test is not None]
        answers_final = []
        for t in tests:
            for q in t.questions.all():
                answers = TestAnswer.objects.filter(question=q, checked=False)
                print(tests, t, answers)
                if len(answers) > 0:
                    for a in answers:
                        answers_final.append(a)
        form = forms.CheckAnswerForm()
        return render(request, 'main/test_checker.html', {'answers': list(set(answers_final)), 'form': form})


# представление обработки проверки ответа ученика преподавателем
class TestCheckSaver(View):
    def post(self, request, pk):
        form = forms.CheckAnswerForm(request.POST)
        if form.is_valid():
            answer = TestAnswer.objects.get(pk=pk)
            answer.checked = True
            answer.score = form.cleaned_data['score']
            answer.comment = form.cleaned_data['comment']
            answer.save()
        return redirect('test_checker')


# представление нотного редактора на режим чтения
class NotesReadonlyView(View):
    def get(self, request, pk):
        ans = TestAnswer.objects.get(pk=pk)
        return render(request, 'main/notes_readonly.html', {'answer': ans.answer, 'asstring': True})


# представление нотного редактора на режим чтения в уроке
class NotesReadonlyLessonView(View):
    def get(self, request, pk):
        note = NoteSet.objects.get(pk=pk)
        return render(request, 'main/notes_readonly.html', {'answer': note.notes, 'asstring': False})


# представление добавления варианта ответа на вопрос теста
class AddTestVariant(View):
    def post(self, request, pk):
        question = TestQuestion.objects.get(pk=pk)
        form = forms.AddTestAnswerVariantForm(request.POST)
        correct = question.correct_answer.all()
        correct = [c.id for c in correct]
        if form.is_valid():
            if form.cleaned_data['answer'] is not None:
                v = form.save(commit=False)
                v.question = question
                v.save()
                vars = [(v.id, v.answer) for v in TestAnswerVariant.objects.filter(question=question)]
                return JsonResponse({'status': 'ok', 'variants': vars, 'correct': correct})
        vars = [(v.id, v.answer) for v in TestAnswerVariant.objects.filter(question=question)]
        return JsonResponse({'status': 'error', 'variants': vars, 'correct': correct})


# представление теста с нотами в качестве ответа
class NotesTest(View):
    def get(self, request):
        return render(request, 'main/notes_answer.html')


# представление очистки вариантов ответа
class DeleteAnswerVariant(View):
    def post(self, request):
        variant = TestAnswerVariant.objects.filter(question_id=100015)
        print(variant)
        for v in variant:
            v.delete()
        return JsonResponse({'status': 'ok'})


# представление отображения списка всех созданных тестов
class AllCreatedTestsView(View):
    def get(self, request):
        tests = Test.objects.filter(test_creator=request.user)
        return render(request, 'main/all_created_tests.html', {'tests': tests})
