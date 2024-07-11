from django.test import TestCase
from django.contrib.auth.models import User, Group
from Main.models import Test, Profile, Discipline, Answer, Question
from django.urls import reverse


# Create your tests here.


class TestCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.group = Group.objects.create(name='Преподаватель')
        self.user.groups.add(self.group)
        self.client.login(username='teacher', password='password')
        self.discipline = Discipline.objects.create(name="Математика")

    def test_create_view(self):
        url = reverse('constructor:test_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constructor/Constructor.html')

    def test_create_test(self):
        url = reverse('constructor:test_create')
        data = {
            'name': 'Test 1',
            'discipline': self.discipline.id,
            'lead_time': '01:00:00',
            'max_score': 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Test.objects.filter(name='Test 1').exists())


class TestUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.group = Group.objects.create(name='Преподаватель')
        self.user.groups.add(self.group)
        self.client.login(username='teacher', password='password')
        self.discipline = Discipline.objects.create(name='Математика')
        self.test = Test.objects.create(name='Test 1', discipline=self.discipline, lead_time='01:00:00',
                                        teacher=self.profile)
        self.question = Question.objects.create(question='Sample Question?', score=5)
        self.test.questions.add(self.question)
        self.answer = Answer.objects.create(possible_answer="Answer 1", correctness=True)
        self.question.answers.add(self.answer)
        self.test.questions.add(self.question)

    def test_update_view(self):
        url = reverse('constructor:test_update', kwargs={'pk': self.test.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constructor/Constructor.html')

    def test_update_test(self):
        url = reverse('constructor:test_update', kwargs={'pk': self.test.id})
        data = {
            'name': 'Updated Test',
            'discipline': self.discipline.id,
            'lead_time': '01:30:00',
            'max_score': 150
        }
        response = self.client.post(url, data)
        self.test.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.test.name, 'Updated Test')


class QuestionUpdateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.group = Group.objects.create(name='Преподаватель')
        self.user.groups.add(self.group)
        self.client.login(username='teacher', password='password')
        self.discipline = Discipline.objects.create(name="Математика")
        self.test = Test.objects.create(name='Test 1', discipline=self.discipline, lead_time='01:00:00', max_score=100,
                                        teacher=self.profile)
        self.question = Question.objects.create(question='Sample Question?', score=5)
        self.test.questions.add(self.question)
        self.answer = Answer.objects.create(possible_answer='Answer 1', correctness=True)
        self.question.answers.add(self.answer)

    def test_question_update_view(self):
        url = reverse('constructor:question_update', kwargs={'pk_test': self.test.id, 'pk_question': self.question.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constructor/question_update.html')

    def test_update_question(self):
        url = reverse('constructor:question_update', kwargs={'pk_test': self.test.id, 'pk_question': self.question.id})
        data = {
            'question': 'Updated Question?',
            'score': 10,
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.answer.id,
            'form-0-possible_answer': 'Updated Answer 1',
            'form-0-correctness': True,
            'form-0-DELETE': '',
        }
        response = self.client.post(url, data)
        self.question.refresh_from_db()
        self.answer.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.question.question, 'Updated Question?')
        self.assertEqual(self.answer.possible_answer, 'Updated Answer 1')


class QuestionCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.group = Group.objects.create(name='Преподаватель')
        self.user.groups.add(self.group)
        self.client.login(username='teacher', password='password')
        self.discipline = Discipline.objects.create(name="Математика")
        self.test = Test.objects.create(name='Test 1', discipline=self.discipline, lead_time='01:00:00',
                                        teacher=self.profile)

    def test_question_create_view(self):
        url = reverse('constructor:question', kwargs={'pk': self.test.id, 'number': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constructor/question.html')

    def test_create_question(self):
        url = reverse('constructor:question', kwargs={'pk': self.test.id, 'number': 1})
        data = {
            'question': 'Sample Question?',
            'score': 5,
            'form-TOTAL_FORMS': '4',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-possible_answer': 'Answer 1',
            'form-0-correctness': True,
            'form-1-possible_answer': 'Answer 2',
            'form-1-correctness': False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Question.objects.filter(question='Sample Question?').exists())


class QuestionUpdateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.group = Group.objects.create(name='Преподаватель')
        self.user.groups.add(self.group)
        self.client.login(username='teacher', password='password')
        self.discipline = Discipline.objects.create(name="Математика")
        self.test = Test.objects.create(name='Test 1', discipline=self.discipline, lead_time='01:00:00',
                                        teacher=self.profile)
        self.question = Question.objects.create(question='Sample Question?', score=5)
        self.answer = Answer.objects.create(possible_answer='Answer 1', correctness=True)
        self.question.answers.add(self.answer)
        self.test.questions.add(self.question)
        session = self.client.session
        session['remaining_questions'] = [self.question.id]
        session['changed_questions'] = []
        session.save()

    def test_question_update_view(self):
        url = reverse('constructor:question_update', kwargs={'pk_test': self.test.id, 'pk_question': self.question.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constructor/question_update.html')

    def test_update_question(self):
        url = reverse('constructor:question_update', kwargs={'pk_test': self.test.id, 'pk_question': self.question.id})
        data = {
            'question': 'Updated Question?',
            'score': 10,
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.answer.id,
            'form-0-possible_answer': 'Updated Answer 1',
            'form-0-correctness': True,
            'form-0-DELETE': '',
        }
        response = self.client.post(url, data)
        self.question.refresh_from_db()
        self.answer.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.question.question, 'Updated Question?')
        self.assertEqual(self.answer.possible_answer, 'Updated Answer 1')
