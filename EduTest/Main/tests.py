from django.test import TestCase

from . models import Answer, Discipline, Question, Profile, Test, Option, TestResult, TestAnswer, EducationalGroup
from django.contrib.auth.models import User

from datetime import time
from .models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.


class AnswerModelTest(TestCase):
    def test_answer_model_save_and_retrieve(self):
        # creating answer a
        # saving answer in to database
        answer1 = Answer(possible_answer='answer1', correctness=False)
        answer1.save()

        # creating answer 2
        # saving answer in to database
        answer2 = Answer(possible_answer='answer2', correctness=True)
        answer2.save()

        # downloading all answers from the database
        all_answers = Answer.objects.all()

        # checking the number of answers
        self.assertEqual(len(all_answers), 2)

        # data convergence check
        self.assertEqual(all_answers[0].possible_answer, 'answer1')
        self.assertEqual(all_answers[1].possible_answer, 'answer2')
        self.assertEqual(all_answers[0].correctness, False)
        self.assertEqual(all_answers[1].correctness, True)


class DisciplineModelTest(TestCase):
    def test_discipline_model_save_and_retrieve(self):
        # creating discipline 1
        # saving discipline in to database
        discipline1 = Discipline(name='discipline1')
        discipline1.save()

        # creating discipline 2
        # saving discipline in to database
        discipline2 = Discipline(name='discipline2')
        discipline2.save()

        # downloading all disciplines from the database
        all_disciplines = Discipline.objects.all()

        # checking the number of disciplines
        self.assertEqual(len(all_disciplines), 2)

        # data convergence check
        self.assertEqual(all_disciplines[0].name, 'discipline1')
        self.assertEqual(all_disciplines[1].name, 'discipline2')


class QuestionModelTest(TestCase):
    def test_question_model_save_and_retrieve(self):
        # creating the data needed to create the main test model
        answer1 = Answer(possible_answer='answer1', correctness=False)
        answer1.save()
        answer2 = Answer(possible_answer='answer2', correctness=True)
        answer2.save()

        # creating question 1
        # saving question in to database
        question1 = Question(question='question1', score=1)
        question1.save()
        question1.answers.add(answer1)
        question1.answers.add(answer2)
        question1.save()

        # creating question 2
        # saving question in to database
        question2 = Question(question='question2', score=2)
        question2.save()
        question2.answers.add(answer1)
        question2.answers.add(answer2)
        question2.save()

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
        self.assertEqual(all_answers1[0].possible_answer, 'answer1')
        self.assertEqual(all_answers1[1].possible_answer, 'answer2')
        self.assertEqual(all_answers2[0].possible_answer, 'answer1')
        self.assertEqual(all_answers2[1].possible_answer, 'answer2')
        self.assertEqual(all_questions[0].score, 1)
        self.assertEqual(all_questions[1].score, 2)


class ProfileModelTest(TestCase):
    def test_profile_model_save_and_retrieve(self):
        # creating the data needed to create the main test model
        user1 = User(username='user1', password='helloworld!1')
        user1.save()
        user2 = User(username='user2', password='helloworld!2')
        user2.save()

        # creating profile 1
        # saving profile in to database
        profile1 = Profile(user=user1, photo='photo1.jpg', access=1)
        profile1.save()

        # creating profile 2
        # saving profile in to database
        profile2 = Profile(user=user2, photo='photo2.jpg', access=2)
        profile2.save()

        # downloading all profiles from the database
        all_profiles = Profile.objects.all()

        # checking the number of authors
        self.assertEqual(len(all_profiles), 2)

        # data convergence check
        self.assertEqual(profile1.user.username, 'user1')
        self.assertEqual(profile1.photo, 'photo1.jpg')
        self.assertEqual(profile1.access, 1)
        self.assertEqual(profile2.user.username, 'user2')
        self.assertEqual(profile2.photo, 'photo2.jpg')
        self.assertEqual(profile2.access, 2)


class TestModelTest(TestCase):
    def test_test_model_save_and_retrieve(self):
        # creating the data needed to create the main test model
        answer11 = Answer(possible_answer='answer11', correctness=False)
        answer11.save()
        answer12 = Answer(possible_answer='answer12', correctness=True)
        answer12.save()
        answer21 = Answer(possible_answer='answer21', correctness=False)
        answer21.save()
        answer22 = Answer(possible_answer='answer22', correctness=True)
        answer22.save()
        question1 = Question(question='question1', score=1)
        question1.save()
        question1.answers.add(answer11)
        question1.answers.add(answer12)
        question1.save()
        question2 = Question(question='question2', score=2)
        question2.save()
        question2.answers.add(answer21)
        question2.answers.add(answer22)
        question2.save()
        discipline1 = Discipline(name='discipline1')
        discipline1.save()
        discipline2 = Discipline(name='discipline2')
        discipline2.save()
        user1 = User(username='user1', password='helloworld!1')
        user1.save()
        user2 = User(username='user2', password='helloworld!2')
        user2.save()
        profile1 = Profile(user=user1, photo='photo1.jpg', access=2)
        profile1.save()
        profile2 = Profile(user=user2, photo='photo2.jpg', access=2)
        profile2.save()

        # creating test 1
        # saving test in to database
        test1 = Test(name='test1', lead_time=time(1, 0, 0), max_score=1,
                     discipline=discipline1, teacher=profile1)
        test1.save()
        test1.questions.add(question1)
        test1.save()

        # creating test 2
        # saving test in to database
        test2 = Test(name='test2', lead_time=time(2, 0, 0), max_score=2,
                     discipline=discipline2, teacher=profile2)
        test2.save()
        test2.questions.add(question2)
        test2.save()

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


class OptionModelTest(TestCase):
    def test_option_model_save_and_retrieve(self):
        # creating the data needed to create the main test model
        user1 = User(username='user1', password='helloworld!1')
        user1.save()
        profile1 = Profile(user=user1, photo='photo1.jpg', access=1)
        profile1.save()
        user2 = User(username='user2', password='helloworld!2')
        user2.save()
        profile2 = Profile(user=user2, photo='photo2.jpg', access=1)
        profile2.save()
        answer11 = Answer(possible_answer='answer11', correctness=False)
        answer11.save()
        answer12 = Answer(possible_answer='answer12', correctness=True)
        answer12.save()
        answer21 = Answer(possible_answer='answer21', correctness=False)
        answer21.save()
        answer22 = Answer(possible_answer='answer22', correctness=True)
        answer22.save()
        question1 = Question(question='question1', score=1)
        question1.save()
        question1.answers.add(answer11)
        question1.answers.add(answer12)
        question1.save()
        question2 = Question(question='question2', score=2)
        question2.save()
        question2.answers.add(answer21)
        question2.answers.add(answer22)
        question2.save()
        discipline1 = Discipline(name='discipline1')
        discipline1.save()
        discipline2 = Discipline(name='discipline2')
        discipline2.save()
        test1 = Test(name='test1', lead_time=time(1, 0, 0), max_score=1,
                     discipline=discipline1, teacher=profile1)
        test1.save()
        test1.questions.add(question1)
        test1.save()
        test2 = Test(name='test2', lead_time=time(2, 0, 0), max_score=2,
                     discipline=discipline2, teacher=profile2)
        test2.save()
        test2.questions.add(question2)
        test2.save()

        # creating option 1
        # saving option in to database
        option1 = Option(student=profile1, test=test1, execution_status=False)
        option1.save()
        option1.questions.add(question1)
        option1.save()

        # creating option 2
        # saving option in to database
        option2 = Option(student=profile2, test=test2, execution_status=True)
        option2.save()
        option2.questions.add(question2)
        option2.save()

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


class TestResultModelTest(TestCase):
    def test_test_result_model_save_and_retrieve(self):
        # creating the data needed to create the main test model
        user1 = User(username='user1', password='helloworld!1')
        user1.save()
        profile1 = Profile(user=user1, photo='photo1.jpg', access=1)
        profile1.save()
        user2 = User(username='user2', password='helloworld!2')
        user2.save()
        profile2 = Profile(user=user2, photo='photo2.jpg', access=1)
        profile2.save()
        answer11 = Answer(possible_answer='answer11', correctness=False)
        answer11.save()
        answer12 = Answer(possible_answer='answer12', correctness=True)
        answer12.save()
        answer21 = Answer(possible_answer='answer21', correctness=False)
        answer21.save()
        answer22 = Answer(possible_answer='answer22', correctness=True)
        answer22.save()
        question1 = Question(question='question1', score=1)
        question1.save()
        question1.answers.add(answer11)
        question1.answers.add(answer12)
        question1.save()
        question2 = Question(question='question2', score=2)
        question2.save()
        question2.answers.add(answer21)
        question2.answers.add(answer22)
        question2.save()
        discipline1 = Discipline(name='discipline1')
        discipline1.save()
        discipline2 = Discipline(name='discipline2')
        discipline2.save()
        test1 = Test(name='test1', lead_time=time(1, 0, 0), max_score=1,
                     discipline=discipline1, teacher=profile1)
        test1.save()
        test1.questions.add(question1)
        test1.save()
        test2 = Test(name='test2', lead_time=time(2, 0, 0), max_score=2,
                     discipline=discipline2, teacher=profile2)
        test2.save()
        test2.questions.add(question2)
        test2.save()
        option1 = Option(student=profile1, test=test1, execution_status=False)
        option1.save()
        option1.questions.add(question1)
        option1.save()
        option2 = Option(student=profile2, test=test2, execution_status=True)
        option2.save()
        option2.questions.add(question2)
        option2.save()

        # creating test result 1
        # saving test result in to database
        test_result1 = TestResult(option=option1, score=1, discipline=discipline1,
                                  lead_time=time(1, 0, 0), test_percentage=1)
        test_result1.save()

        # creating test result 2
        # saving test result in to database
        test_result2 = TestResult(option=option2, score=2, discipline=discipline2,
                                  lead_time=time(2, 0, 0), test_percentage=2)
        test_result2.save()

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
        self.assertEqual(all_test_results[0].lead_time, time(1, 0, 0))
        self.assertEqual(all_test_results[1].lead_time, time(2, 0, 0))
        self.assertEqual(all_test_results[0].test_percentage, 1)
        self.assertEqual(all_test_results[1].test_percentage, 2)


class TestAnswerModelTest(TestCase):
    def test_test_answer_model_save_and_retrieve(self):
        # creating the data needed to create the main test model
        question1 = Question(question='question1', score=1)
        question1.save()
        question2 = Question(question='question2', score=2)
        question2.save()
        answer11 = Answer(possible_answer='answer11', correctness=False)
        answer11.save()
        answer12 = Answer(possible_answer='answer12', correctness=True)
        answer12.save()
        answer21 = Answer(possible_answer='answer21', correctness=False)
        answer21.save()
        answer22 = Answer(possible_answer='answer22', correctness=True)
        answer22.save()
        question1.answers.add(answer11)
        question1.answers.add(answer12)
        question1.save()
        question2.answers.add(answer21)
        question2.answers.add(answer22)
        question2.save()
        discipline1 = Discipline(name='discipline1')
        discipline1.save()
        discipline2 = Discipline(name='discipline2')
        discipline2.save()
        user1 = User(username='user1', password='helloworld!1')
        user1.save()
        user2 = User(username='user2', password='helloworld!2')
        user2.save()
        profile1 = Profile(user=user1, photo='photo1.jpg', access=2)
        profile1.save()
        profile2 = Profile(user=user2, photo='photo2.jpg', access=2)
        profile2.save()
        test1 = Test(name='test1', lead_time=time(1, 0, 0), max_score=1,
                     discipline=discipline1, teacher=profile1)
        test1.save()
        test1.questions.add(question1)
        test1.save()
        test2 = Test(name='test2', lead_time=time(2, 0, 0), max_score=2,
                     discipline=discipline2, teacher=profile2)
        test2.save()
        test2.questions.add(question2)
        test2.save()

        # creating test answer 1
        # saving test answer in to database
        test_answer1 = TestAnswer(question=question1, user_answer="answer1", score=1, test=test1,
                                  option_question_number=1)
        test_answer1.save()

        # creating test answer 2
        # saving test answer in to database
        test_answer2 = TestAnswer(question=question2, user_answer="answer2", score=2, test=test2,
                                  option_question_number=2)
        test_answer2.save()

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
        self.assertEqual(all_test_answers[0].test.name, 'test1')
        self.assertEqual(all_test_answers[1].test.name, 'test2')
        self.assertEqual(all_test_answers[0].option_question_number, 1)
        self.assertEqual(all_test_answers[1].option_question_number, 2)


class EducationalGroupModelTest(TestCase):
    def test_educational_group_save_and_retrieve(self):
        # creating the data needed to create the main test model
        user1 = User(username='user1', password='helloworld!1')
        user1.save()
        user2 = User(username='user2', password='helloworld!2')
        user2.save()
        profile1 = Profile(user=user1, photo='photo1.jpg', access=1)
        profile1.save()
        profile2 = Profile(user=user2, photo='photo2.jpg', access=2)
        profile2.save()

        # creating educational group 1
        # saving educational group in to database
        educational_group1 = EducationalGroup(number_group="1", user=profile1)
        educational_group1.save()

        # creating education group 2
        # saving educational group in to database
        educational_group2 = EducationalGroup(number_group="2", user=profile2)
        educational_group2.save()

        # downloading all educational groups from the database
        all_educational_groups = EducationalGroup.objects.all()

        # checking number of educational groups
        self.assertEqual(len(all_educational_groups), 2)

        # data convergence check
        self.assertEqual(all_educational_groups[0].number_group, "1")
        self.assertEqual(all_educational_groups[1].number_group, "2")
        self.assertEqual(all_educational_groups[0].user.user.username, 'user1')
        self.assertEqual(all_educational_groups[1].user.user.username, 'user2')


class HomePageViewTests(TestCase):
    # preset for testing
    def setUp(self):
        # creating a user and profile
        self.user = User.objects.create_user(username='testuser', password='testuserhomepage')
        self.profile = Profile.objects.create(user=self.user, access=2)

    # testing the home page with an authorized user
    def test_home_view_with_authenticated_user(self):
        # user authorization
        self.client.login(username='testuser', password='testuserhomepage')

        # getting a response from the home page URL
        response = self.client.get(reverse('Main:home'))

        # checking page code status
        self.assertEqual(response.status_code, 200)

        # context checking
        self.assertTrue(response.context['user_authorized'])
        self.assertEqual(response.context['access'], 2)

    # testing the home page with an unauthorized user
    def test_home_view_with_unauthorized_user(self):
        # getting a response from the home page URL
        response = self.client.get(reverse('Main:home'))

        # checking page code status
        self.assertEqual(response.status_code, 200)

        # context checking
        self.assertFalse(response.context['user_authorized'])
        self.assertEqual(response.context['access'], 0)
