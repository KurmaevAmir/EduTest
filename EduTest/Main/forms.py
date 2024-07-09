from django import forms
from .models import Profile, EducationalGroup


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