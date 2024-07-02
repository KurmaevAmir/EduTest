from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Answer(models.Model):
    possible_answer = models.CharField(max_length=150)
    correctness = models.BooleanField(default=False)

    def __str__(self):
        return self.possible_answer


class Discipline(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=150)
    answers = models.ManyToManyField(Answer)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.question


class Profile(models.Model):
    ACCESSES = [(1, "Студент"),
                (2, "Преподаватель"),
                (3, "Администратор"), ]
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    access = models.IntegerField('access', choices=ACCESSES, default=1)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Test(models.Model):
    name = models.CharField(max_length=150)
    questions = models.ManyToManyField(Question)
    lead_time = models.TimeField()
    max_score = models.IntegerField(default=0)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Option(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    execution_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " " + str(self.student.user.first_name) + " " + str(
            self.student.user.last_name) + " " + str(self.test.id)


class TestResult(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    lead_time = models.TimeField()
    test_percentage = models.IntegerField(default=0)

    def __str__(self):
        return str(
            self.option.id) + " " + self.option.student.user.first_name + " " + self.option.student.user.last_name + " " + str(
            self.score)


class TestAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=150)
    score = models.IntegerField(default=0)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    option_question_number = models.IntegerField(default=1)

    def __str__(self):
        return str(self.option_question_number) + " " + self.test.name


class EducationalGroup(models.Model):
    number_group = models.CharField(max_length=50)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " - " + self.number_group
