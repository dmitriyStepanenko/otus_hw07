from django.urls import path, re_path
from .views import (
    questions_list_view,
    create_post,
    question_answers_view,
    like_unlike_question_view,
    dislike_undislike_question_view,
    like_unlike_answer_view,
    dislike_undislike_answer_view,
    right_answer_view,
    search_tag_view,
    search_view,
)

app_name = 'posts'

urlpatterns = [
    path('', questions_list_view, name='main-post-view'),
    path('ask/', create_post, name='create-new-post-view'),
    path('question/<header>', question_answers_view, name='question-answers-view'),
    path('like_question/', like_unlike_question_view, name='question-like-view'),
    path('dislike_question/', dislike_undislike_question_view, name='question-dislike-view'),
    path('like_answer/', like_unlike_answer_view, name='answer-like-view'),
    path('dislike_answer/', dislike_undislike_answer_view, name='answer-dislike-view'),
    path('right_answer/', right_answer_view, name='right-answer-view'),
    path('tag/<tag>/', search_tag_view, name='search-tag-view'),
    path('search', search_view, name='search-view'),
]
