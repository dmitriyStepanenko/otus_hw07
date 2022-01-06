from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView, FormView, UpdateView

from .models import Question, Answer, Tag
from .forms import QuestionModelForm
from .forms import AnswerModelForm
from .utils import send_email, change_rating


class QuestionsListView(ListView):
    model = Question
    template_name = 'posts/main.html'
    paginate_by = 20
    ordering = ['-created', '-rating']

    def get(self, request, *args, **kwargs):
        self.ordering = ['-rating', '-created'] if request.GET.get('q_sort') == 'hot' else ['-created', '-rating']
        return super(QuestionsListView, self).get(request, *args, **kwargs)


class CreatePostView(LoginRequiredMixin, FormView):
    template_name = 'posts/create_post.html'
    form_class = QuestionModelForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        for tag in instance.get_tag_list():
            if not Tag.objects.get(text=tag):
                Tag(text=tag).save()
        return redirect('posts:question-answers-view', header=instance.header)


class QuestionAnswersView(ListView):
    model = Answer
    template_name = 'posts/question_answers.html'
    paginate_by = 30
    ordering = ['-rating', '-created']
    extra_context = {}

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(header=self.kwargs.get('header'))
        if not question:
            redirect('posts:main-post-view')
        self.queryset = Answer.objects.filter(question=question)
        self.extra_context['question'] = question
        self.extra_context['form'] = AnswerModelForm(None)

        return super(QuestionAnswersView, self).get(request, *args, **kwargs)


class CreateAnswerView(LoginRequiredMixin, FormView):
    form_class = AnswerModelForm
    template_name = 'posts/question_answers.html'

    def form_valid(self, form):
        question = Question.objects.get(header=self.kwargs.get('header'))
        if not question:
            redirect('posts:main-post-view')
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.question = question
        instance.save()

        if question.author.email:
            send_email(question, self.request.user)

        return redirect('posts:question-answers-view', header=question.header)


class LikeUnlikeObj(LoginRequiredMixin, UpdateView):
    do_like = None

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj, header = self.get_object_and_header()
        if not obj:
            redirect('posts:main-post-view')

        if self.do_like is None:
            raise AttributeError('attribute do_like must be defined')

        change_rating(request.user, obj, self.do_like)
        return redirect('posts:question-answers-view', header=header)

    def get_object_and_header(self):
        print(self.request.path)
        if self.model == 'Question':
            question = Question.objects.get(id=self.request.POST.get('question_id'))
            return question, question.header
        elif self.model == 'Answer':
            answer = Answer.objects.get(id=self.request.POST.get('answer_id'))
            return answer, answer.question.header
        else:
            raise AttributeError('attribute model must be defined')


class RightAnswerView(LoginRequiredMixin, UpdateView):
    def get_object(self, queryset=None):
        answer = Answer.objects.get(id=self.request.POST.get('answer_id'))
        if not answer:
            redirect('posts:main-post-view')
        return answer

    def post(self, request, *args, **kwargs):
        answer = self.get_object()
        for ans in answer.question.get_answers():
            if ans == answer:
                continue
            if ans.chosen_as_correct:
                ans.chosen_as_correct = False
                ans.save()

        answer.chosen_as_correct = not answer.chosen_as_correct
        answer.save()
        return redirect('posts:question-answers-view', header=answer.question.header)


class SearchView(ListView):
    template_name = 'posts/search.html'
    ordering = ['-rating', '-created']
    paginate_by = 20
    extra_context = {}

    def get(self, request, *args, **kwargs):
        tag = request.GET.get('tag')
        if tag is not None:
            return redirect('posts:search-tag-view', tag=tag)

        q = request.GET.get('q')
        if q is not None:
            str_q = str(q)
            if len(str_q) > 4 and str_q[:4] == 'tag:':
                return redirect('posts:search-tag-view', tag=str(q)[4:])
            elif len(str_q) > 0:
                self.queryset = Question.objects.filter(Q(header__icontains=str_q) | Q(text__icontains=str_q))
                self.extra_context['s_question'] = str_q
                return super(SearchView, self).get(request, *args, **kwargs)


class SearchTagView(ListView):
    template_name = 'posts/search.html'
    ordering = ['-rating', '-created']
    paginate_by = 20
    extra_context = {}

    def get(self, request, *args, **kwargs):
        tag = self.kwargs.get('tag')
        qs = Question.objects.all()
        qs = [q.id for q in qs if tag in q.get_tag_list()]
        self.queryset = Question.objects.filter(id__in=qs)
        self.extra_context['tag'] = tag

        return super(SearchTagView, self).get(request, *args, **kwargs)
