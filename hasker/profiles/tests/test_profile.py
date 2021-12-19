from django.test import TestCase

from profiles.models import Profile


class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(username='user1', password='Hasker123')

    def test_email_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_email_label_max_len(self):
        profile = Profile.objects.get(id=1)
        max_len = profile._meta.get_field('email').max_length
        self.assertEqual(max_len, 200)

    def test_str(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(str(profile), f'{profile.username} - {profile.created.strftime("%d-%m-%Y")}')

    def test_get_avatar(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.get_avatar, '/media/avatar.png')
