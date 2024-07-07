from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, View
from Main.models import Test, Answer, Question
from .forms import TestForm, QuestionForm, AnswerFormSet, AnswerUpdateFormSet


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
        questions = list(self.object.questions.values_list('id', flat=True))
        self.request.session['remaining_questions'] = questions
        self.request.session['changed_questions'] = []
        self.request.session.modified = True
        return reverse('constructor:question_update', kwargs={'pk_test': pk, 'pk_question': questions[0]})


class QuestionCreateView(View, LoginRequiredMixin, UserAccessMixin):
    template_name = 'constructor/question.html'

    def get(self, request, pk, number):
        test = get_object_or_404(Test, pk=pk)
        question_form = QuestionForm()
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


class QuestionUpdateView(View, LoginRequiredMixin, UserAccessMixin):
    template_name = 'constructor/question_update.html'

    def get(self, request, pk_test, pk_question):
        test = get_object_or_404(Test, pk=pk_test)
        question = get_object_or_404(Question, pk=pk_question)
        question_form = QuestionForm(instance=question)
        answer_formset = AnswerUpdateFormSet(queryset=question.answers.all())
        return render(request, self.template_name, {
            'test': test,
            'question_form': question_form,
            'answer_formset': answer_formset,
            'question': question,
        })

    def post(self, request, pk_test, pk_question):
        test = get_object_or_404(Test, pk=pk_test)
        question = get_object_or_404(Question, pk=pk_question)
        question_form = QuestionForm(request.POST, instance=question)
        answer_formset = AnswerUpdateFormSet(request.POST, queryset=question.answers.all())
        if question_form.is_valid() and answer_formset.is_valid():
            question_form.save()
            for form in answer_formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
                else:
                    answer = form.save(commit=False)
                    answer.save()
            question.save()
            request.session['changed_questions'].append(pk_question)
            request.session['remaining_questions'].remove(pk_question)
            request.session.modified = True
            if request.session['remaining_questions']:
                next_question_id = request.session['remaining_questions'][0]
                return redirect('constructor:question_update', pk_test=pk_test, pk_question=next_question_id)
            # temporary stub
            return redirect('constructor:test_update', pk=pk_test)
        return render(request, self.template_name, {
            'test': test,
            'question_form': question_form,
            'answer_formset': answer_formset,
            'question': question,
        })
