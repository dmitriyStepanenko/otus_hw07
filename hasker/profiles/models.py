from django.db import models
from django.contrib.auth.models import AbstractUser

from .utils import get_image_path


class Profile(AbstractUser):
    email = models.EmailField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to=get_image_path)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} - {self.created.strftime("%d-%m-%Y")}'

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else None
