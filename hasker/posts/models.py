from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from profiles.models import Profile

import re


class Tag(models.Model):
    text = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.text


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    header = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    tags = models.CharField(max_length=60, blank=True)

    liked = models.ManyToManyField(Profile, blank=True, related_name='q_likes')
    unliked = models.ManyToManyField(Profile, blank=True, related_name='q_unlikes')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}-{self.header}-{self.text[:20]}'

    def clean(self):
        super(Question, self).clean()

        str_tags = str(self.tags)
        tags = str_tags.split(',')
        if len(tags) > 3:
            raise ValidationError('Not allowed more three tags')
        for tag in tags:
            tag_length = len(tag.replace(' ', ''))
            for part_tag in tag.split(' '):
                if len(part_tag) not in [0, tag_length]:
                    raise ValidationError('Not allowed space in tag word')
            if tags.count(tag) > 1:
                raise ValidationError('Not allowed equal tag words')

    @property
    def rating(self):
        return self.liked.all().count() - self.unliked.all().count()

    def get_tag_list(self):
        return str(self.tags).replace(' ', '').split(',')

    def get_answers(self):
        return self.answer_set.all()

    def is_right_answer(self):
        for answer in self.get_answers():
            if answer.chosen_as_correct:
                return True
        return False

    def get_absolute_url(self):
        return reverse("posts:question-answers-view", kwargs={"header": self.header})

    def num_likes(self):
        return self.liked.all().count()-self.unliked.all().count()

    def num_answers(self):
        return self.answer_set.all().count()


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_as_correct = models.BooleanField(default=False)

    text = models.TextField()

    liked = models.ManyToManyField(Profile, blank=True, related_name='a_likes')
    unliked = models.ManyToManyField(Profile, blank=True, related_name='a_unlikes')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def rating(self):
        return self.liked.all().count() - self.unliked.all().count()

    def num_likes(self):
        return self.liked.all().count()-self.unliked.all().count()

    def __str__(self):
        return f'{self.author}-{self.text[:20]}'
