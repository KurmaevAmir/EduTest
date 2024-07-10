import random

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, FormView, ListView, UpdateView
from .models import Profile, Test, Option, TestAnswer, Answer, TestResult, EducationalGroup
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm, TestAssignmentSelectForm, LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from constructor.views import UserAccessMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# Create your views here.


class HomePageView(FormView):
    template_name = 'Main/home.html'
    form_class = LoginForm
    success_url = reverse_lazy('Main:home')

    def dispatch(self, request, *args, **kwargs):
        self.user_authorized = request.user.is_authenticated
        if self.user_authorized:
            self.profile = get_object_or_404(Profile, user=request.user)
        else:
            self.profile = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_authorized'] = self.user_authorized
        context['access'] = 2 if self.request.user.groups.filter(
            name__in=['Преподаватель', 'Администратор']).exists() else 1 if self.request.user.groups.filter(
            name__in=['Студент']).exists() else 0
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(email=email)
            user_authenticate = authenticate(username=user.username, password=password)
            if user_authenticate is not None:
                login(self.request, user_authenticate)
                next_url = self.request.GET.get('next', self.success_url)
                return redirect(next_url)
            else:
                form.add_error(None, "Неверный пароль. Пожалуйста, попробуйте снова.")
        except User.DoesNotExist:
            form.add_error('email', "Пользователь с таким email не найден.")
        return self.form_invalid(form)


def login_required_decorator(view_class):
    decorator = method_decorator(login_required)
    view_class.dispatch = decorator(view_class.dispatch)
    return view_class


@method_decorator(login_required, name='dispatch')
class TestDescriptionView(DetailView):
    model = Test
    template_name = 'Main/test_description.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['access'] = 2 if self.request.user.groups.filter(
            name__in=['Преподаватель', 'Администратор']).exists() else 1 if self.request.user.groups.filter(
            name__in=['Студент']).exists() else 0
        return context

    def post(self, request, *args, **kwargs):
        test = self.get_object()
        student = request.user.profile
        # option = Option.objects.create(student=student, test=test, start_time=timezone.now())
        try:
            option = get_object_or_404(Option, student=student, execution_status=False, test=test)
        except Option.MultipleObjectsReturned:
            option = Option.objects.filter(student=student, execution_status=False, test=test).first()
        option.start_time = timezone.now()
        questions = list(test.questions.all())
        random.shuffle(questions)
        option.questions.set(questions)
        option.save()
        return redirect('Main:test_form', option_id=option.id, question_number=1)


@method_decorator(login_required, name='dispatch')
class TestFormView(FormView):
    form_class = AnswerForm
    template_name = 'Main/test_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.option = get_object_or_404(Option, id=self.kwargs['option_id'], student=request.user.profile)
        self.question_number = int(self.kwargs['question_number'])
        self.question = self.option.questions.all()[self.question_number - 1]

        elapsed_time = timezone.now() - self.option.start_time
        total_seconds = (
                self.option.test.lead_time.hour * 3600 + self.option.test.lead_time.minute * 60 + self.option.test.lead_time.second)
        if elapsed_time.total_seconds() > total_seconds:
            self.option.execution_status = True
            self.option.save()
            return redirect('Main:test_result', pk=self.option.id)
        if self.option.execution_status:
            return redirect('Main:test_result', pk=self.option.id)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['question'] = self.question
        return kwargs

    def form_valid(self, form):
        user_answer_id = form.cleaned_data['user_answer']
        user_answer = get_object_or_404(Answer, id=user_answer_id)
        TestAnswer.objects.create(
            question=self.question,
            user_answer=user_answer.possible_answer,
            score=self.question.score if user_answer.correctness else 0,
            option=self.option,
            option_question_number=self.question_number
        )
        next_question_number = self.question_number + 1
        if next_question_number <= self.option.questions.count():
            return redirect('Main:test_form', option_id=self.option.id, question_number=next_question_number)
        else:
            self.option.execution_status = True
            self.option.save()
            return redirect('Main:test_result', pk=self.option.test.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['option'] = self.option
        context['question'] = self.question
        answers = list(self.question.answers.all())
        random.shuffle(answers)
        context['answers'] = answers
        elapsed_time = timezone.now() - self.option.start_time
        total_seconds = (
                self.option.test.lead_time.hour * 3600 + self.option.test.lead_time.minute * 60 + self.option.test.lead_time.second)
        remaining_time = total_seconds - elapsed_time.total_seconds()
        hours, remainder = divmod(remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        context['remaining_time'] = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        context['current_question_number'] = self.question_number
        context['total_questions'] = self.option.questions.count()
        return context


@method_decorator(login_required, name='dispatch')
class TestResultView(DetailView):
    model = Option
    template_name = 'Main/test_result.html'
    context_object_name = 'option'

    def get_object(self):
        return Option.objects.filter(student=self.request.user.profile, test=self.kwargs['pk']).order_by(
            '-start_time').first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        option = self.object
        question_ids = option.questions.values_list('id', flat=True)
        test_answers = TestAnswer.objects.filter(question_id__in=question_ids, option=option)
        total_score = sum(answer.score for answer in test_answers)
        max_score = sum(question.score for question in option.questions.all())
        test_percentage = int((total_score / max_score) * 100) if max_score > 0 else 0

        test_result, created = TestResult.objects.update_or_create(
            option=option,
            defaults={
                'score': total_score,
                'discipline': option.test.discipline,
                'lead_time': option.test.lead_time,
                'test_percentage': test_percentage
            }
        )

        context.update({
            'test_answers': test_answers,
            'total_score': total_score,
            'max_score': max_score,
            'test_percentage': test_percentage,
            'student': option.student,
            'teacher': option.test.teacher,
        })
        return context


@method_decorator(login_required, name='dispatch')
class TestAssignmentView(UserAccessMixin, LoginRequiredMixin, FormView):
    template_name = 'Main/test_assignment_create.html'
    form_class = TestAssignmentSelectForm

    def get_success_url(self):
        return reverse_lazy('Main:test_description', kwargs={'pk': self.test.pk})

    def form_valid(self, form):
        students = form.cleaned_data['students']
        groups = form.cleaned_data['groups']
        self.test = Test.objects.get(pk=self.kwargs['pk'])
        group_students = Profile.objects.filter(educationalgroup__id__in=groups)
        all_students = Profile.objects.filter(id__in=students).union(group_students)
        for student in all_students:
            Option.objects.create(
                student=student,
                test=self.test,
                start_time=timezone.now(),
                execution_status=False
            )
        return super().form_valid(form)


class RegistrationView(FormView):
    template_name = 'Main/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('Main:home')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password']
        )
        profile = Profile.objects.create(user=user)
        educational_group, created = EducationalGroup.objects.update_or_create(number_group=form.cleaned_data['education_group'])
        if not created:
            educational_group.save()
        educational_group.user.add(profile)
        login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect(reverse('Main:home'))


class TestListView(UserAccessMixin, ListView):
    model = Test
    template_name = 'Main/test_list.html'
    context_object_name = 'tests'
