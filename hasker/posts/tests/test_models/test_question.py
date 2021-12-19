from django.test import TestCase

from posts.models import Question, Answer
from profiles.models import Profile


class QuestionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Profile.objects.create(username='test_user', password='Hasker123')
        Question.objects.create(author=author, header='how', text='123')

    def test_header_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('header').verbose_name
        self.assertEqual(field_label, 'header')

    def test_text_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_tag_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('tags').verbose_name
        self.assertEqual(field_label, 'tags')

    def test_header_label_max_len(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('header').max_length
        self.assertEqual(max_length, 200)

    def test_tag_label_max_len(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('tags').max_length
        self.assertEqual(max_length, 60)

    def test_str(self):
        question = Question.objects.get(id=1)
        self.assertEqual(str(question), f'{question.author}-{question.header}-{question.text[:20]}')

    def test_rating(self):
        question = Question.objects.get(id=1)
        question.liked.add(Profile.objects.create(username='tu1', password='Hasker123'))
        question.liked.add(Profile.objects.create(username='tu2', password='Hasker123'))
        question.unliked.add(Profile.objects.create(username='tu3', password='Hasker123'))

        self.assertEqual(question.rating, 1)

    def test_get_tag_list(self):
        question = Question.objects.get(id=1)
        question.tags = 't1, t2, t3'
        self.assertEqual(question.get_tag_list(), ['t1', 't2', 't3'])

    def test_get_answers(self):
        question = Question.objects.get(id=1)
        ans_author = Profile.objects.create(username='tu1', password='Hasker123')
        ans1 = Answer.objects.create(question=question, author=ans_author, text='aaa')
        ans2 = Answer.objects.create(question=question, author=ans_author, text='bbb')

        self.assertEqual(list(question.get_answers()), [ans1, ans2])

    def test_right_answer_existence(self):
        question = Question.objects.get(id=1)
        self.assertEqual(question.is_right_answer(), False)

        ans_author = Profile.objects.create(username='tu1', password='Hasker123')
        Answer.objects.create(question=question, author=ans_author, text='aaa')
        self.assertEqual(question.is_right_answer(), False)
        Answer.objects.create(question=question, author=ans_author, text='aaa', chosen_as_correct=True)
        self.assertEqual(question.is_right_answer(), True)

    def test_get_absolute_url(self):
        question = Question.objects.get(id=1)
        self.assertEqual(question.get_absolute_url(), '/hasker.com/question/how')

    def test_num_answers(self):
        question = Question.objects.get(id=1)
        self.assertEqual(question.num_answers(), 0)

        ans_author = Profile.objects.create(username='tu1', password='Hasker123')
        Answer.objects.create(question=question, author=ans_author, text='aaa')
        self.assertEqual(question.num_answers(), 1)

