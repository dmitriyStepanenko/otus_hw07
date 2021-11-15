from django.contrib import admin
from .models import Question, Answer, Tag

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
