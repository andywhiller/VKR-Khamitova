from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from . import models


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    username = forms.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует'})

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def clean_email(self):
        for user in User.objects.all():
            if user.email == self.cleaned_data['email']:
                raise ValidationError("Email must be unique!")
        return self.cleaned_data['email']





class EditUserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=191, required=False,
                               error_messages={
                                   'max_length': 'Длина должна быть меньше 191 символов',
                                   'unique': 'Это имя пользователя уже занято'
                               })
    first_name = forms.CharField(max_length=191, required=False,
                                 error_messages={
                                     'max_length': 'Длина должна быть меньше 191 символов'
                                 })
    last_name = forms.CharField(max_length=191, required=False,
                                error_messages={
                                    'max_length': 'Длина должна быть меньше 191 символов'
                                })

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class EditUserdataForm(forms.ModelForm):
    fathersname = forms.CharField(max_length=50, required=False,
                                  error_messages={
                                      'max_length': 'Длина должна быть меньше 50 символов'
                                  })
    birthdate = forms.DateField(required=False)
    musicedu = forms.CharField(required=False)
    phone = forms.IntegerField(required=False)
    profile_avatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])],
    )

    class Meta:
        model = models.Userdata
        fields = ['fathersname', 'birthdate', 'musicedu', 'phone', 'profile_avatar']

