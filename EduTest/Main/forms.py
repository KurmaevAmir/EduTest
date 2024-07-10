import re

from django import forms
from .models import Profile, EducationalGroup
from django.core.exceptions import ValidationError


class AnswerForm(forms.Form):
    user_answer = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['user_answer'].choices = [(answer.id, answer.possible_answer) for answer in question.answers.all()]


class TestAssignmentSelectForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.filter(user__groups__name='Студент'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Выберите студентов'
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=EducationalGroup.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Выберите группы'
    )


class LoginForm(forms.Form):
    email = forms.CharField(label='Электронная почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=150)
    last_name = forms.CharField(label='Фамилия', max_length=150)
    email = forms.EmailField(label='Электронная почта', max_length=254)
    education_group = forms.CharField(label='Образовательная группа', max_length=50)
    password = forms.CharField(label='Пароль', max_length=128, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Пароль', max_length=128, widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Пароль должен быть не менее 8 символов.')
        if not re.search(r'[a-zA-Z]', password) and not re.search(r'а-яА-Я', password):
            raise ValidationError('Пароль должен содержать буквы')
        if not re.search(r'\d', password):
            raise ValidationError('Пароль должен содержать цифры')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Пароль не содержит специальные символы')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise ValidationError('Пароли не совпадают.')
        return cleaned_data
