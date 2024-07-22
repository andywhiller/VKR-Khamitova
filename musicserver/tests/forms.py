from django import forms
from . import models


class AddTestQuestionForm(forms.ModelForm):
    class Meta:
        model = models.TestQuestion
        fields = '__all__'


class AddTestForm(forms.ModelForm):
    class Meta:
        model = models.Test
        fields = ['name', ]


class OneAnswerTest(forms.Form):
    answer = forms.CharField(label="Ответ", widget=forms.RadioSelect())
    question = forms.CharField(widget=forms.HiddenInput())


class ManyAnswerTest(forms.Form):
    answer = forms.CharField(label="Ответ", widget=forms.CheckboxSelectMultiple())
    question = forms.CharField(widget=forms.HiddenInput())


class OpenAnswerTest(forms.Form):
    answer = forms.CharField(label="Ответ", widget=forms.TextInput(attrs={'class': 'form-control'}))
    question = forms.CharField(widget=forms.HiddenInput())


class FileAnswerTest(forms.Form):
    answer = forms.FileField(label="Ответ", widget=forms.FileInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(label="Комментарий", required=False)
    question = forms.CharField(widget=forms.HiddenInput())


class CheckAnswerForm(forms.Form):
    score = forms.CharField(label="Баллы", widget=forms.TextInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(label="Комментарий", required=False)


class NoteAnswerForm(forms.Form):
    comment = forms.CharField(label="Комментарий", required=False, widget=forms.TextInput())
    answer = forms.CharField(label="Ответ", widget=forms.HiddenInput(attrs={'id': 'note_answer'}))
    question = forms.CharField(widget=forms.HiddenInput())

    note = "<iframe src='http://127.0.0.1:8000/tests/notes' width='650px' height='350px'></iframe>"


class AddTestAnswerVariantForm(forms.ModelForm):
    class Meta:
        model = models.TestAnswerVariant
        fields = ['answer']