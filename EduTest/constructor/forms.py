from django.forms import ModelForm, modelformset_factory
from Main.models import Test, Question, Answer


class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'discipline',  'lead_time', 'max_score']


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'score']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['possible_answer', 'correctness']


AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=4)
AnswerUpdateFormSet = modelformset_factory(Answer, form=AnswerForm, can_delete=True, extra=0)
