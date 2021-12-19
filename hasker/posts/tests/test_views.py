from django.test import TestCase

from posts.models import Question, Answer
from profiles.models import Profile


class PostViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(username='user1', password='Hasker123')

    def test_question_list_view(self):
        resp = self.client.get('/hasker.com/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('qs' in resp.context)
        self.assertEqual(len(resp.context['qs']), 0)

        author = Profile.objects.get(id=1)
        for i in range(30):
            Question.objects.create(author=author, header=f'how {i}', text='a')

        resp = self.client.get('/hasker.com/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('qs' in resp.context)
        self.assertEqual(len(resp.context['qs']), 20)

    def test_create_post(self):
        user = Profile.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.post(
            '/hasker.com/ask/',
            data={
                'header': 'how',
                'text': 'aaa',
                'tags': '',
            }
        )
        self.assertRedirects(resp, '/hasker.com/question/how')

    def test_look_at_answers(self):
        user = Profile.objects.get(id=1)
        question = Question.objects.create(author=user, header='how', text='aaa')
        Answer.objects.create(author=user, question=question, text='bbb')
        resp = self.client.get('/hasker.com/question/how')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('answers' in resp.context)
        self.assertEqual(len(resp.context['answers']), 1)

        self.client.force_login(user)
        resp = self.client.post(
            '/hasker.com/question/how',
            data={
                'text': 'ccc',
            }
        )
        self.assertRedirects(resp, '/hasker.com/question/how')
        question = Question.objects.get(id=1)
        self.assertEqual(question.num_answers(), 2)
        resp = self.client.get('/hasker.com/question/how')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('answers' in resp.context)
        self.assertEqual(len(resp.context['answers']), 2)

    def test_like_unlike_question(self):
        user = Profile.objects.get(id=1)
        Question.objects.create(author=user, header='how', text='aaa')

        self.client.force_login(user)
        resp = self.client.post('/hasker.com/like_question/', data={'question_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        question = Question.objects.get(id=1)
        self.assertEqual(question.rating, 1)

        resp = self.client.post('/hasker.com/like_question/', data={'question_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        question = Question.objects.get(id=1)
        self.assertEqual(question.rating, 0)

        resp = self.client.post('/hasker.com/dislike_question/', data={'question_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        question = Question.objects.get(id=1)
        self.assertEqual(question.rating, -1)

        resp = self.client.post('/hasker.com/dislike_question/', data={'question_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        question = Question.objects.get(id=1)
        self.assertEqual(question.rating, 0)

    def test_like_unlike_answer(self):
        user = Profile.objects.get(id=1)
        question = Question.objects.create(author=user, header='how', text='aaa')
        Answer.objects.create(author=user, question=question, text='bbb')

        self.client.force_login(user)
        resp = self.client.post('/hasker.com/like_answer/', data={'answer_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        answer = Answer.objects.get(id=1)
        self.assertEqual(answer.rating, 1)

        resp = self.client.post('/hasker.com/like_answer/', data={'answer_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        answer = Answer.objects.get(id=1)
        self.assertEqual(answer.rating, 0)

        resp = self.client.post('/hasker.com/dislike_answer/', data={'answer_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        answer = Answer.objects.get(id=1)
        self.assertEqual(answer.rating, -1)

        resp = self.client.post('/hasker.com/dislike_answer/', data={'answer_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        answer = Answer.objects.get(id=1)
        self.assertEqual(answer.rating, 0)

    def test_choose_correct(self):
        user = Profile.objects.get(id=1)
        question = Question.objects.create(author=user, header='how', text='aaa')
        Answer.objects.create(author=user, question=question, text='bbb')

        self.client.force_login(user)
        resp = self.client.post('/hasker.com/right_answer/', data={'answer_id': 1})
        self.assertRedirects(resp, '/hasker.com/question/how')

        answer = Answer.objects.get(id=1)
        self.assertEqual(answer.chosen_as_correct, True)

    def test_search(self):
        user = Profile.objects.get(id=1)
        Question.objects.create(author=user, header='how', text='aaa', tags='tag1')
        Question.objects.create(author=user, header='how2', text='aaa', tags='tag2')
        Question.objects.create(author=user, header='how3', text='aaa')

        resp = self.client.get('/hasker.com/tag/tag1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('qs' in resp.context)
        self.assertEqual(len(resp.context['qs']), 1)
        self.assertEqual(resp.context['qs'][0].header, 'how')

        resp = self.client.get('/hasker.com/search/', data={'tag': 'tag2'})
        self.assertRedirects(resp, '/hasker.com/tag/tag2/')

        resp = self.client.get('/hasker.com/search/', data={'q': 'tag:tag2'})
        self.assertRedirects(resp, '/hasker.com/tag/tag2/')

        resp = self.client.get('/hasker.com/search/', data={'q': 'aaa'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('qs' in resp.context)
        self.assertEqual(len(resp.context['qs']), 3)
