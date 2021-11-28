from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    email = models.EmailField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username.username} - {self.created.strftime("%d-%m-%Y")}'
