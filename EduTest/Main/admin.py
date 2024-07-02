from django.contrib import admin

from .models import Answer, Discipline, EducationalGroup, Option, Profile, Question, TestAnswer, Test, TestResult
# Register your models here.


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = ['possible_answer', 'correctness']
    list_display = ['possible_answer', 'correctness']
    search_fields = ['possible_answer']


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    search_fields = ['name']


@admin.register(EducationalGroup)
class EducationalGroupAdmin(admin.ModelAdmin):
    fields = ['number_group', 'user']
    list_display = ['number_group', 'user']
    search_fields = ['number_group', 'user']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    fields = ['student', 'test', 'questions', 'execution_status']
    list_display = ['student', 'test', 'execution_status']
    search_fields = ['student', 'test']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'photo']}),
        ('Расширенные настройки', {'fields': ['access']})
    ]
    list_display = ['user', 'photo', 'access']
    search_fields = ['user', 'access']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['question', 'answers', 'score']
    list_display = ['question', 'score']
    search_fields = ['question']


@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    fields = ['option_question_number', 'test', 'question', 'user_answer', 'score']
    list_display = ['option_question_number', 'test', 'question', 'user_answer', 'score']
    search_fields = ['option_question_number', 'test', 'question']


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    fields = ['option', 'discipline', 'lead_time', 'test_percentage', 'score']
    list_display = ['option', 'discipline', 'lead_time', 'test_percentage', 'score']
    search_fields = ['option', 'discipline']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    fields = ['name', 'questions', 'discipline', 'teacher', 'lead_time', 'max_score']
    list_display = ['name', 'discipline', 'teacher', 'max_score']
    search_fields = ['name', 'discipline', 'teacher']
