from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from . import forms
from .models import Userdata
from course.models import Courses, CourseProgress
from lessons.models import Lesson

from course.models import CourseFeedback


@login_required
def index(request):
    template_name = 'main/index.html'
    return render(request, template_name)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'myauth/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('mainindex')
        return render(request, 'myauth/login.html', {'form': form})


class OpenIndexView(View):
    def get(self, request):
        all_courses = Courses.objects.filter(is_course_active=True)
        context = {'all_courses': all_courses}
        template_name = 'main/openindex.html'
        return render(request, template_name, context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('commonindex')


class RegisterView(View):
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, 'myauth/register.html', {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Userdata.objects.create(user=user)
            return redirect('login')
        return render(request, 'myauth/register.html', {'form': form})


def info(request):
    template_name = 'main/info.html'
    return render(request, template_name)


def settings(request):
    template_name = 'main/settings.html'
    return render(request, template_name)


def myprofile(request):
    template_name = 'main/myprofile.html'
    return render(request, template_name)


class CommonIndexView(View):
    def get(self, request):
        all_courses = Courses.objects.filter(is_course_active=True)
        feedbacks = [sum([r.rating for r in rating])/len(rating) if len(rating) != 0 else 0 for rating in (CourseFeedback.objects.filter(course=course) for course in all_courses)]
        feedbacks = [round(f, 1) for f in feedbacks]
        sorted_data = sorted(zip(feedbacks, all_courses), key=lambda x: x[0], reverse=True)
        sorted_feedbacks, sorted_all_courses = zip(*sorted_data)
        context = {'all_courses': zip(sorted_all_courses, sorted_feedbacks)}
        template_name = 'main/commonindex.html'
        return render(request, template_name, context)


class EditUserProfileView(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        form = forms.EditUserProfileForm(instance=user)
        form2 = forms.EditUserdataForm(instance=Userdata.objects.get(user=user))
        return render(request, 'main/edit_profile.html', {'form': form, 'form2': form2, 'user': user})

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        form = forms.EditUserProfileForm(request.POST, request.FILES, instance=user)
        form2 = forms.EditUserdataForm(request.POST, request.FILES, instance=Userdata.objects.get(user=user))
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('myprofile')
        return render(request, 'main/edit_profile.html', {'form': form, 'form2': form2, 'user': user})


