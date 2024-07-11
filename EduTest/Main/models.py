from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Answer(models.Model):
    possible_answer = models.CharField(verbose_name="вариант ответа", max_length=150)
    correctness = models.BooleanField(verbose_name="корректность", default=False)

    def __str__(self):
        return self.possible_answer

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'


class Discipline(models.Model):
    name = models.CharField(verbose_name="название", max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'дисциплину'
        verbose_name_plural = 'дисциплины'


class Question(models.Model):
    question = models.CharField(verbose_name="вопрос", max_length=150)
    answers = models.ManyToManyField(Answer, verbose_name="ответы",)
    score = models.IntegerField(verbose_name="количество баллов", default=0)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class Profile(models.Model):
    ACCESSES = [(1, "Студент"),
                (2, "Преподаватель"),
                (3, "Администратор"), ]
    user = models.OneToOneField(User, related_name='profile',verbose_name="пользователь",  on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name="фотография профиля", upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


class Test(models.Model):
    name = models.CharField(verbose_name="название", max_length=150)
    questions = models.ManyToManyField(Question, verbose_name="вопросы", blank=True)
    lead_time = models.TimeField(verbose_name="время выполнения")
    discipline = models.ForeignKey(Discipline, verbose_name="дисциплина", on_delete=models.CASCADE)
    teacher = models.ForeignKey(Profile, verbose_name="преподаватель", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'


class Option(models.Model):
    student = models.ForeignKey(Profile, verbose_name="студент", on_delete=models.CASCADE)
    test = models.ForeignKey(Test, verbose_name="тест", on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, verbose_name="вопросы")
    execution_status = models.BooleanField(verbose_name="статус выполнения", default=False)
    start_time = models.DateTimeField(verbose_name='время начала', default=timezone.now)

    def __str__(self):
        return str(self.id) + " " + str(self.student.user.first_name) + " " + str(
            self.student.user.last_name) + " " + str(self.test.id)

    class Meta:
        verbose_name = 'вариант'
        verbose_name_plural = 'варианты'


class TestResult(models.Model):
    option = models.ForeignKey(Option, verbose_name="вариант", on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name="количество баллов", default=0)
    discipline = models.ForeignKey(Discipline, verbose_name="дисциплина", on_delete=models.CASCADE)
    lead_time = models.TimeField(verbose_name="время выполнения")
    test_percentage = models.IntegerField(verbose_name="процент выполнения", default=0)

    def __str__(self):
        return str(
            self.option.id) + " " + self.option.student.user.first_name + " " + self.option.student.user.last_name + " " + str(
            self.score)

    class Meta:
        verbose_name = 'результат теста'
        verbose_name_plural = 'результаты тестов'
        unique_together = ('option', 'discipline')


class TestAnswer(models.Model):
    question = models.ForeignKey(Question, verbose_name="вопрос", on_delete=models.CASCADE)
    user_answer = models.CharField(verbose_name="ответ студента", max_length=150)
    score = models.IntegerField(verbose_name="количество баллов", default=0)
    option = models.ForeignKey(Option, verbose_name="вариант", on_delete=models.CASCADE)
    option_question_number = models.IntegerField(verbose_name="номер вопроса в варианте", default=1)

    def __str__(self):
        return str(self.option_question_number) + " " + self.option.test.name

    class Meta:
        verbose_name = 'ответ студента на вопрос'
        verbose_name_plural = 'ответы студента на вопросы'


class EducationalGroup(models.Model):
    number_group = models.CharField(verbose_name="номер группы", max_length=50)
    user = models.ManyToManyField(Profile, verbose_name="студент")

    def __str__(self):
        return self.number_group

    class Meta:
        verbose_name = 'образовательную группу'
        verbose_name_plural = 'образовательные группы'
