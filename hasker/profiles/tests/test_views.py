from django.test import TestCase

from profiles.models import Profile


class ProfilesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(username='user1', password='Hasker123')

    def test_signup_view(self):
        resp = self.client.get('/hasker.com/signup/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            '/hasker.com/signup/',
            data={
                'username': 'user2',
                'email': 'a@a.com',
                'password1': 'Hasker123',
                'password2': 'Hasker123',
                'avatar': '',
            }
        )
        self.assertEqual(len(Profile.objects.all()), 2)
        self.assertRedirects(resp, '/hasker.com/')

    def test_edit_view(self):
        user = Profile.objects.get(id=1)

        resp = self.client.get('/hasker.com/user/edit/')
        self.assertRedirects(resp, '/hasker.com/accounts/login/?next=/hasker.com/user/edit/')

        self.client.force_login(user)
        resp = self.client.get('/hasker.com/user/edit/')
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(user.email, '')
        resp = self.client.post(
            '/hasker.com/user/edit/',
            data={
                'email': 'a@a.com',
                'avatar': '',
            }
        )
        self.assertEqual(resp.status_code, 200)

        user = Profile.objects.get(id=1)
        self.assertEqual(user.email, 'a@a.com')
