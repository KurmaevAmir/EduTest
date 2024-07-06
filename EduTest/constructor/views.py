from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, View
from Main.models import Test, Answer
from .forms import TestForm, QuestionForm, AnswerFormSet

# Create your views here.


# reject request with permission error if test_func methods returns False
class UserAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Преподаватель', 'Администратор']).exists()

    def handle_no_permission(self):
        return HttpResponseNotFound()


class TestCreateView(CreateView, LoginRequiredMixin, UserAccessMixin):
    model = Test
    form_class = TestForm
    template_name = 'constructor/Constructor.html'

    def form_valid(self, form):
        form.instance.teacher = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.pk
        return reverse('constructor:question', kwargs={'pk': pk, 'number': 1})


class TestUpdateView(UpdateView, LoginRequiredMixin, UserAccessMixin):
    model = Test
    form_class = TestForm
    template_name = 'constructor/Constructor.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Test, pk=pk)

    def get_success_url(self):
        pk = self.object.pk
        return reverse('constructor:question', kwargs={'pk': pk, 'number': 1})


class QuestionCreateView(View, LoginRequiredMixin, UserAccessMixin):
    template_name = 'constructor/question.html'

    def get(self, request, pk, number):
        test = get_object_or_404(Test, pk=pk)
        question_form = QuestionForm
        answer_formset = AnswerFormSet(queryset=Answer.objects.none())
        return render(request, self.template_name, {
            'test': test,
            'question_form': question_form,
            'answer_formset': answer_formset,
        })

    def post(self, request, pk, number):
        test = get_object_or_404(Test, pk=pk)
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)

        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save()
            for form in answer_formset:
                if form.cleaned_data:
                    answer = form.save()
                    question.answers.add(answer)
            test_questions = test.questions
            test_questions.add(question)
            return redirect('constructor:question', pk=pk, number=number + 1)
        return render(request, self.template_name, {
            'test': test,
            'question_form': question_form,
            'answer_formset': answer_formset,
        })
