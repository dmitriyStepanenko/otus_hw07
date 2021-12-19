from django.test import TestCase

from posts.models import Tag


class TagTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(text='aa')

    def test_text_label(self):
        tag = Tag.objects.get(id=1)
        field_label = tag._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_text_label_max_len(self):
        tag = Tag.objects.get(id=1)
        max_len = tag._meta.get_field('text').max_length
        self.assertEqual(max_len, 20)

    def test_str(self):
        tag = Tag.objects.get(id=1)
        self.assertEqual(str(tag), 'aa')
