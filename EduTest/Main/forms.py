import re

from django import forms
from .models import Profile, EducationalGroup
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm


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


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', max_length=150)
    last_name = forms.CharField(label='Фамилия', max_length=150)
    email = forms.EmailField(label='Электронная почта')
    group = forms.ModelChoiceField(label='Образовательная группа', queryset=EducationalGroup.objects.all())

    class Meta:
        model = Profile
        fields = ['photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance.user
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields[
            'group'].initial = user.profile.educationalgroup_set.first() if user.profile.educationalgroup_set.exists() else None

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
            if self.cleaned_data['group']:
                user.profile.educationalgroup_set.clear()
                self.cleaned_data['group'].user.add(profile)
        return profile


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Старый пароль"
        self.fields['new_password1'].label = "Новый пароль"
        self.fields['new_password2'].label = "Подтверждение нового пароля"
