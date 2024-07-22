from django.shortcuts import render, redirect
from django.views import View
from . import forms
from .models import Courses, CourseProgress, CourseFeedback
from lessons.models import Lesson


# представление отображения созданных и проходимых курсов
class MyCoursesView(View):
    def get(self, request):
        user = request.user
        my_created_courses = Courses.objects.filter(course_creator=user)
        my_passing_courses = Courses.objects.filter(course_students__in=[user])
        progresses = [CourseProgress.objects.get_or_create(user=request.user, course=c)[0] for c in my_passing_courses]
        max_priority = [max([l.lesson_priority for l in Lesson.objects.filter(lesson_course=c)]) for c in
                        my_passing_courses]
        context = {'my_created_courses': my_created_courses, 'my_passing_courses': my_passing_courses,
                   'progresses': progresses,
                   'zip': zip(my_passing_courses, progresses, max_priority)}
        template_name = 'main/my_courses.html'
        return render(request, template_name, context)


# представление отображения курса
class CourseView(View):
    def get(self, request, pk):
        course = Courses.objects.get(id=pk)
        lessons = Lesson.objects.filter(lesson_course=course).order_by('lesson_priority')
        progress = CourseProgress.objects.get_or_create(user=request.user, course=course)[0]
        feedbacks = CourseFeedback.objects.filter(course=course)
        max_priority = max([lesson.lesson_priority for lesson in lessons])
        context = {
            'course': course,
            'lessons': lessons,
            'progress': progress,
            'max_priority': max_priority,
            'btn': 'my',
            'feedbacks': feedbacks,
        }
        if course.course_students.filter(id=request.user.id).exists():
            context['btn'] = 'passing'
        elif course.course_creator == request.user:
            context['btn'] = 'created'
        else:
            context['btn'] = 'signup'
        template_name = 'main/current_course.html'
        form = forms.AddFeedbackForm()
        context['form'] = form
        return render(request, template_name, context)

    def post(self, request, pk):
        course = Courses.objects.get(id=pk)
        form = forms.AddFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.user = request.user
            feedback.save()
            return redirect('current_course', pk=pk)


# представления создания курса
class AddCourseView(View):
    def get(self, request):
        form = forms.AddCourseForm()
        return render(request, 'main/add_course.html',
                      {'form': form, 'action': 'Добавление', 'button_text': "Добавить"})

    def post(self, request):
        form = forms.AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.course_creator = request.user
            course.save()
            Lesson.objects.create(lesson_course=course, lesson_priority=0, lesson_name="Знакомство")
            return redirect('my_courses')
        return render(request, 'main/my_courses.html',
                      {'form': form, 'action': 'Добавление', 'button_text': "Добавить"})


# представление удаления курса
class DeleteCourseView(View):
    def get(self, request, pk):
        if request.user != Courses.objects.get(id=pk).course_creator:
            return redirect('my_courses')
        course = Courses.objects.get(id=pk)
        course.delete()
        return redirect('my_courses')


# представление изменения курса
class UpdateCourseView(View):
    def get(self, request, pk):
        if request.user != Courses.objects.get(id=pk).course_creator:
            return redirect('my_courses')
        course = Courses.objects.get(id=pk)
        form = forms.AddCourseForm(instance=course)
        return render(request, 'main/add_course.html',
                      {'form': form, 'action': 'Изменение', 'course': course, 'button_text': "Сохранить"})

    def post(self, request, pk):
        if request.user != Courses.objects.get(id=pk).course_creator:
            return redirect('my_courses')
        course = Courses.objects.get(id=pk)
        form = forms.AddCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('my_courses')
        return render(request, 'main/add_course.html',
                      {'form': form, 'action': 'Изменение', 'course': course, 'button_text': "Сохранить"})

# представление записи на курс
class CourseSignUpView(View):
    def get(self, request, pk):
        course = Courses.objects.get(id=pk)
        course.course_students.add(request.user)
        return redirect('current_course', pk=course.id)


# представление ухода с курса
class CourseSignOutView(View):
    def get(self, request, pk):
        course = Courses.objects.get(id=pk)
        course.course_students.remove(request.user)
        return redirect('current_course', pk=course.id)


# представление оценки курса
class RateCourseView(View):
    def get(self, request, pk):
        course = Courses.objects.get(id=pk)
        return render(request, 'main/rate_course.html')