from django.test import TestCase

from posts.models import Question, Answer
from profiles.models import Profile


class AnswerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Profile.objects.create(username='test_user', password='Hasker123')
        question = Question.objects.create(author=author, header='how', text='123')
        Answer.objects.create(author=author, question=question, text='aaa')

    def test_chosen_as_correct_label(self):
        answer = Answer.objects.get(id=1)
        field_label = answer._meta.get_field('chosen_as_correct').verbose_name
        self.assertEqual(field_label, 'chosen as correct')

    def test_text_label(self):
        answer = Answer.objects.get(id=1)
        field_label = answer._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_str(self):
        answer = Answer.objects.get(id=1)
        self.assertEqual(str(answer), f'{answer.author}-{answer.text[:20]}')

    def test_rating(self):
        answer = Answer.objects.get(id=1)
        answer.liked.add(Profile.objects.create(username='tu1', password='Hasker123'))
        answer.liked.add(Profile.objects.create(username='tu2', password='Hasker123'))
        answer.unliked.add(Profile.objects.create(username='tu3', password='Hasker123'))

        self.assertEqual(answer.rating, 1)


