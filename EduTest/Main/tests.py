import datetime

from django.test import TestCase

from .models import Answer, Discipline, Question, Profile, Test, Option, TestResult, TestAnswer, EducationalGroup
from django.contrib.auth.models import User, Group
from datetime import time
from django.urls import reverse
import pytz


# Create your tests here.


class MainModelsTest(TestCase):
    def setUp(self):
        self.question1 = Question(question='question1', score=1)
        self.question1.save()
        self.question2 = Question(question='question2', score=2)
        self.question2.save()
        self.answer11 = Answer(possible_answer='answer11', correctness=False)
        self.answer11.save()
        self.answer12 = Answer(possible_answer='answer12', correctness=True)
        self.answer12.save()
        self.answer21 = Answer(possible_answer='answer21', correctness=False)
        self.answer21.save()
        self.answer22 = Answer(possible_answer='answer22', correctness=True)
        self.answer22.save()
        self.question1.answers.add(self.answer11)
        self.question1.answers.add(self.answer12)
        self.question2.answers.add(self.answer21)
        self.question2.answers.add(self.answer22)
        self.discipline1 = Discipline(name='discipline1')
        self.discipline1.save()
        self.discipline2 = Discipline(name='discipline2')
        self.discipline2.save()
        self.user1 = User(username='user1', password='helloworld!1')
        self.user1.save()
        self.user2 = User(username='user2', password='helloworld!2')
        self.user2.save()
        self.profile1 = Profile(user=self.user1, photo='photo1.jpg')
        self.profile1.save()
        self.profile2 = Profile(user=self.user2, photo='photo2.jpg')
        self.profile2.save()
        groups = ['Студент', "Преподаватель", "Администратор"]
        self.group_student = Group.objects.create(name=groups[0])
        self.user1.groups.add(self.group_student)
        self.group_teacher = Group.objects.create(name=groups[1])
        self.user2.groups.add(self.group_teacher)
        self.test1 = Test(name='test1', lead_time=time(1, 0, 0), max_score=1,
                          discipline=self.discipline1, teacher=self.profile1)
        self.test1.save()
        self.test1.questions.add(self.question1)
        self.test2 = Test(name='test2', lead_time=time(2, 0, 0), max_score=2,
                          discipline=self.discipline2, teacher=self.profile2)
        self.test2.save()
        self.test2.questions.add(self.question2)
        self.option1 = Option(student=self.profile1, test=self.test1, execution_status=False,
                              start_time=datetime.datetime(2011, 11, 11, 11, 11, 11, tzinfo=pytz.timezone('Europe/Moscow')))
        self.option1.save()
        self.option1.questions.add(self.question1)
        self.option2 = Option(student=self.profile2, test=self.test2, execution_status=True,
                              start_time=datetime.datetime(2012, 12, 12, 12, 12, 12, tzinfo=pytz.timezone('Europe/Moscow')))
        self.option2.save()
        self.option2.questions.add(self.question2)
        self.test_result1 = TestResult(option=self.option1, score=1, discipline=self.discipline1,
                                       lead_time=time(1, 1, 1), test_percentage=1)
        self.test_result1.save()
        self.test_result2 = TestResult(option=self.option2, score=2, discipline=self.discipline2,
                                       lead_time=time(2, 2, 2), test_percentage=2)
        self.test_result2.save()
        self.test_answer1 = TestAnswer(question=self.question1, user_answer="answer1", score=1, option=self.option1,
                                       option_question_number=1)
        self.test_answer1.save()
        self.test_answer2 = TestAnswer(question=self.question2, user_answer="answer2", score=2, option=self.option2,
                                       option_question_number=2)
        self.test_answer2.save()
        self.educational_group1 = EducationalGroup(number_group="1")
        self.educational_group1.save()
        self.educational_group2 = EducationalGroup(number_group="2")
        self.educational_group2.save()
        self.educational_group1.user.add(self.profile1)
        self.educational_group2.user.add(self.profile2)

    def test_answer_model_save_and_retrieve(self):
        # downloading all answers from the database
        all_answers = Answer.objects.all()

        # checking the number of answers
        self.assertEqual(len(all_answers), 4)

        # data convergence check
        self.assertEqual(all_answers[0].possible_answer, 'answer11')
        self.assertEqual(all_answers[1].possible_answer, 'answer12')
        self.assertEqual(all_answers[2].possible_answer, 'answer21')
        self.assertEqual(all_answers[3].possible_answer, 'answer22')
        self.assertEqual(all_answers[0].correctness, False)
        self.assertEqual(all_answers[1].correctness, True)
        self.assertEqual(all_answers[2].correctness, False)
        self.assertEqual(all_answers[3].correctness, True)

    def test_discipline_model_save_and_retrieve(self):
        # downloading all disciplines from the database
        all_disciplines = Discipline.objects.all()

        # checking the number of disciplines
        self.assertEqual(len(all_disciplines), 2)

        # data convergence check
        self.assertEqual(all_disciplines[0].name, 'discipline1')
        self.assertEqual(all_disciplines[1].name, 'discipline2')

    def test_question_model_save_and_retrieve(self):
        # downloading all questions from the database
        all_questions = Question.objects.all()

        # downloading all answers from the database
        all_answers1 = all_questions[0].answers.all()
        all_answers2 = all_questions[1].answers.all()

        # checking the number of questions
        self.assertEqual(len(all_questions), 2)

        # checking the number of answers question
        self.assertEqual(len(all_answers1), 2)
        self.assertEqual(len(all_answers2), 2)

        # data convergence check
        self.assertEqual(all_questions[0].question, 'question1')
        self.assertEqual(all_questions[1].question, 'question2')
        self.assertEqual(all_answers1[0].possible_answer, 'answer11')
        self.assertEqual(all_answers1[1].possible_answer, 'answer12')
        self.assertEqual(all_answers2[0].possible_answer, 'answer21')
        self.assertEqual(all_answers2[1].possible_answer, 'answer22')
        self.assertEqual(all_questions[0].score, 1)
        self.assertEqual(all_questions[1].score, 2)

    def test_profile_model_save_and_retrieve(self):
        # downloading all profiles from the database
        all_profiles = Profile.objects.all()

        # checking the number of authors
        self.assertEqual(len(all_profiles), 2)

        # data convergence check
        self.assertEqual(all_profiles[0].user.username, 'user1')
        self.assertEqual(all_profiles[0].photo, 'photo1.jpg')
        self.assertEqual(all_profiles[1].user.username, 'user2')
        self.assertEqual(all_profiles[1].photo, 'photo2.jpg')

    def test_test_model_save_and_retrieve(self):
        # downloading all test from the database
        all_tests = Test.objects.all()

        # downloading all questions from the database
        all_questions1 = all_tests[0].questions.all()
        all_questions2 = all_tests[1].questions.all()

        # checking the number of test
        self.assertEqual(len(all_tests), 2)

        # checking the number of questions
        self.assertEqual(len(all_questions1), 1)
        self.assertEqual(len(all_questions2), 1)

        # data convergence check
        self.assertEqual(all_tests[0].name, 'test1')
        self.assertEqual(all_tests[1].name, 'test2')
        self.assertEqual(all_questions1[0].question, 'question1')
        self.assertEqual(all_questions2[0].question, 'question2')
        self.assertEqual(all_tests[0].lead_time, time(1, 0, 0))
        self.assertEqual(all_tests[1].lead_time, time(2, 0, 0))
        self.assertEqual(all_tests[0].max_score, 1)
        self.assertEqual(all_tests[1].max_score, 2)
        self.assertEqual(all_tests[0].discipline.name, 'discipline1')
        self.assertEqual(all_tests[1].discipline.name, 'discipline2')
        self.assertEqual(all_tests[0].teacher.user.username, 'user1')
        self.assertEqual(all_tests[1].teacher.user.username, 'user2')

    def test_option_model_save_and_retrieve(self):
        # downloading all options from the database
        all_options = Option.objects.all()

        # downloading all questions from the database
        all_questions1 = all_options[0].questions.all()
        all_questions2 = all_options[1].questions.all()

        # checking the number of options
        self.assertEqual(len(all_options), 2)

        # checking the number of questions
        self.assertEqual(len(all_questions1), 1)
        self.assertEqual(len(all_questions2), 1)

        # data convergence check
        self.assertEqual(all_options[0].student.user.username, 'user1')
        self.assertEqual(all_options[1].student.user.username, 'user2')
        self.assertEqual(all_options[0].test.name, 'test1')
        self.assertEqual(all_options[1].test.name, 'test2')
        self.assertEqual(all_questions1[0].question, 'question1')
        self.assertEqual(all_questions2[0].question, 'question2')
        self.assertEqual(all_options[0].execution_status, False)
        self.assertEqual(all_options[1].execution_status, True)
        self.assertEqual(all_options[0].start_time, datetime.datetime(2011, 11, 11, 11, 11, 11, tzinfo=pytz.timezone('Europe/Moscow')))
        self.assertEqual(all_options[1].start_time, datetime.datetime(2012, 12, 12, 12, 12, 12, tzinfo=pytz.timezone('Europe/Moscow')))

    def test_test_result_model_save_and_retrieve(self):
        # downloading all test results from the database
        all_test_results = TestResult.objects.all()

        # checking the number of test results
        self.assertEqual(len(all_test_results), 2)

        # data convergence check
        self.assertEqual(all_test_results[0].option.execution_status, False)
        self.assertEqual(all_test_results[1].option.execution_status, True)
        self.assertEqual(all_test_results[0].score, 1)
        self.assertEqual(all_test_results[1].score, 2)
        self.assertEqual(all_test_results[0].discipline.name, 'discipline1')
        self.assertEqual(all_test_results[1].discipline.name, 'discipline2')
        self.assertEqual(all_test_results[0].lead_time, time(1, 1, 1))
        self.assertEqual(all_test_results[1].lead_time, time(2, 2, 2))
        self.assertEqual(all_test_results[0].test_percentage, 1)
        self.assertEqual(all_test_results[1].test_percentage, 2)

    def test_test_answer_model_save_and_retrieve(self):
        # downloading all test answers from the database
        all_test_answers = TestAnswer.objects.all()

        # checking the number of test answers
        self.assertEqual(len(all_test_answers), 2)

        # data convergence check
        self.assertEqual(all_test_answers[0].question.question, 'question1')
        self.assertEqual(all_test_answers[1].question.question, 'question2')
        self.assertEqual(all_test_answers[0].user_answer, 'answer1')
        self.assertEqual(all_test_answers[1].user_answer, 'answer2')
        self.assertEqual(all_test_answers[0].score, 1)
        self.assertEqual(all_test_answers[1].score, 2)
        self.assertEqual(all_test_answers[0].option.test.name, 'test1')
        self.assertEqual(all_test_answers[1].option.test.name, 'test2')
        self.assertEqual(all_test_answers[0].option_question_number, 1)
        self.assertEqual(all_test_answers[1].option_question_number, 2)

    def test_educational_group_save_and_retrieve(self):
        # downloading all educational groups from the database
        all_educational_groups = EducationalGroup.objects.all()

        # checking number of educational groups
        self.assertEqual(len(all_educational_groups), 2)

        # data convergence check
        self.assertEqual(all_educational_groups[0].number_group, "1")
        self.assertEqual(all_educational_groups[1].number_group, "2")
        self.assertEqual(all_educational_groups[0].user.all()[0].user.username, 'user1')
        self.assertEqual(all_educational_groups[1].user.all()[0].user.username, 'user2')


class HomePageViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testuserhomepage')
        self.profile = Profile.objects.create(user=self.user)
        groups = ['Студент', "Преподаватель", "Администратор"]
        group_student = Group.objects.create(name=groups[0])
        self.user.groups.add(group_student)
        self.home_url = reverse("Main:home")

    def test_home_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testuserhomepage')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user_authorized'])
        self.assertEqual(response.context['access'], 1)

    def test_home_view_with_unauthorized_user(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user_authorized'])
        self.assertEqual(response.context['access'], 0)

    def test_login_page_status_code(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_login_page_template(self):
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'Main/home.html')

    def test_login_with_valid_data(self):
        response = self.client.post(self.home_url, {
            'email': 'test@example.com',
            'password': 'testuserhomepage'
        })

    def test_login_with_invalid_email(self):
        response = self.client.post(self.home_url, {
            'email': 'invalid@example.com',
            'password': 'testuserhomepage'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пользователь с таким email не найден.')

    def test_login_with_invalid_password(self):
        response = self.client.post(self.home_url, {
            'email': 'test@example.com',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный пароль. Пожалуйста, попробуйте снова.')


class RegistrationForm(TestCase):
    def setUp(self):
        self.page = reverse('Main:registration')

    def test_register_page_status_code(self):
        response = self.client.get(self.page)
        self.assertEqual(response.status_code, 200)

    def test_register_page_template(self):
        response = self.client.get(self.page)
        self.assertTemplateUsed(response, 'Main/registration.html')

    def test_register_user(self):
        data = {
            'first_name': 'UserName',
            'last_name': 'UserLastName',
            'email': 'user@example.com',
            'education_group': '11-305',
            'password': 'Password1!',
            'password_confirmation': 'Password1!'
        }
        response = self.client.post(self.page, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='user@example.com').exists())


class TestListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher', password='password')
        self.profile = Profile.objects.create(user=self.user)
        groups = ['Студент', "Преподаватель", "Администратор"]
        group_teacher = Group.objects.create(name=groups[1])
        self.user.groups.add(group_teacher)
        self.discipline = Discipline.objects.create(name='Math')
        self.test = Test.objects.create(
            name='Sample Test',
            lead_time='00:30:00',
            max_score=100,
            discipline=self.discipline,
            teacher=self.profile
        )
        self.test_list = reverse('Main:test_list')

    def test_test_list_view_status_code(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.test_list)
        self.assertEqual(response.status_code, 200)

    def test_test_list_view_template_user(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.test_list)
        self.assertTemplateUsed(response, 'Main/test_list.html')


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.group = EducationalGroup.objects.create(number_group='Test Group')
        self.discipline = Discipline.objects.create(name='Math')
        self.client.login(username='testuser', password='password')

    def test_profile_view_status_code(self):
        response = self.client.get(reverse('Main:profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_uses_correct_template(self):
        response = self.client.get(reverse('Main:profile'))
        self.assertTemplateUsed(response, 'Main/profile.html')

    def test_profile_update(self):
        response = self.client.post(reverse('Main:profile'), {
            'save_profile': True,
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'group': self.group.id,
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user.first_name, 'Test')
        self.assertEqual(self.profile.user.last_name, 'User')
        self.assertEqual(self.profile.user.email, 'testuser@example.com')
        self.assertEqual(self.profile.educationalgroup_set.first(), self.group)

    def test_password_change(self):
        response = self.client.post('/profile/', {
            'change_password': 'Change Password',
            'old_password': 'password',
            'new_password1': 'N3wP@ssword123!',
            'new_password2': 'N3wP@ssword123!'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('N3wP@ssword123!'))
