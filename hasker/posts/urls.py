from django.urls import path

from .views import (
    QuestionsListView,
    CreatePostView,
    QuestionAnswersView,
    CreateAnswerView,
    LikeUnlikeObj,
    RightAnswerView,
    SearchTagView,
    SearchView,
)

app_name = 'posts'

urlpatterns = [
    path('', QuestionsListView.as_view(), name='main-post-view'),
    path('ask/', CreatePostView.as_view(), name='create-new-post-view'),
    path('question/<header>/', QuestionAnswersView.as_view(), name='question-answers-view'),
    path('question/answer/<header>/', CreateAnswerView.as_view(), name='create-answer-view'),
    path('like_question/', LikeUnlikeObj.as_view(do_like=True, model='Question'), name='question-like-view'),
    path('dislike_question/', LikeUnlikeObj.as_view(do_like=False, model='Question'), name='question-dislike-view'),
    path('like_answer/', LikeUnlikeObj.as_view(do_like=True, model='Answer'), name='answer-like-view'),
    path('dislike_answer/', LikeUnlikeObj.as_view(do_like=False, model='Answer'), name='answer-dislike-view'),
    path('right_answer/', RightAnswerView.as_view(), name='right-answer-view'),
    path('tag/<tag>/', SearchTagView.as_view(), name='search-tag-view'),
    path('search/', SearchView.as_view(), name='search-view'),
]
