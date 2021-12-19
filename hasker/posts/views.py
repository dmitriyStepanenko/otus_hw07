from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Question, Answer, Tag
from .forms import QuestionModelForm
from .forms import AnswerModelForm
from .utils import send_email, change_rating


def questions_list_view(request):
    questions = Question.objects.all()
    page_num = request.GET.get('page') or 1

    if request.method == 'GET':
        q_sort = request.GET.get('q_sort') or 'new'
        if q_sort == 'new':
            questions = sorted(questions, key=lambda item: (item.created, item.rating), reverse=True)
        elif q_sort == 'hot':
            questions = sorted(questions, key=lambda item: (item.rating, item.created), reverse=True)

    context = {
        'qs': Paginator(questions, 20).get_page(page_num)
    }
    return render(request, 'posts/main.html', context)


@login_required
def create_post(request):
    p_form = QuestionModelForm(request.POST or None)

    if request.method == 'POST':
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = request.user
            instance.save()

            for tag in instance.get_tag_list():
                Tag(text=tag).save()

            return redirect('posts:question-answers-view', header=instance.header)

    context = {
        'p_form': p_form,
    }
    return render(request, 'posts/create_post.html', context)


def question_answers_view(request, header=None):

    question = Question.objects.get(header=header)
    if not question:
        redirect('posts:main-post-view')

    answers = Answer.objects.filter(question=question)
    answers = sorted(answers, key=lambda item: (item.rating, item.created), reverse=True)

    a_form = AnswerModelForm(request.POST or None)
    paginator = Paginator(answers, 30)
    page_num = request.GET.get('page') or 1

    if request.method == 'POST':
        user = request.user
        if user and a_form.is_valid():
            instance = a_form.save(commit=False)
            instance.author = user
            instance.question = question
            instance.save()

            if question.author.email:
                send_email(question, user)

            return redirect('posts:question-answers-view', header=question.header)

    context = {
        "question": question,
        "answers": paginator.get_page(page_num),
        "a_form": a_form,
    }
    return render(request, 'posts/question_answers.html', context)


@login_required
@transaction.atomic
def like_unlike_question_view(request):
    if request.method == 'POST':
        question = Question.objects.get(id=request.POST.get('question_id'))
        if not question:
            redirect('posts:main-post-view')

        change_rating(request.user, question.liked, question.unliked)

        return redirect('posts:question-answers-view', header=question.header)


@login_required
@transaction.atomic
def dislike_undislike_question_view(request):
    if request.method == 'POST':
        question = Question.objects.get(id=request.POST.get('question_id'))
        if not question:
            redirect('posts:main-post-view')

        change_rating(request.user, question.unliked, question.liked)

        return redirect('posts:question-answers-view', header=question.header)


@login_required
@transaction.atomic
def like_unlike_answer_view(request):
    if request.method == 'POST':
        answer = Answer.objects.get(id=request.POST.get('answer_id'))
        if not answer:
            redirect('posts:main-post-view')
        change_rating(request.user, answer.liked, answer.unliked)

        return redirect('posts:question-answers-view', header=answer.question.header)


@login_required
@transaction.atomic
def dislike_undislike_answer_view(request):
    if request.method == 'POST':
        answer = Answer.objects.get(id=request.POST.get('answer_id'))
        if not answer:
            redirect('posts:main-post-view')

        change_rating(request.user, answer.unliked, answer.liked)

        return redirect('posts:question-answers-view', header=answer.question.header)


@login_required
@transaction.atomic
def right_answer_view(request):
    if request.method == 'POST':
        answer = Answer.objects.get(id=request.POST.get('answer_id'))

        if not answer:
            redirect('posts:main-post-view')

        for ans in answer.question.get_answers():
            if ans == answer:
                continue

            if ans.chosen_as_correct:
                ans.chosen_as_correct = False
                ans.save()

        answer.chosen_as_correct = not answer.chosen_as_correct
        answer.save()

        return redirect('posts:question-answers-view', header=answer.question.header)


def search_view(request):
    if request.method == 'GET':
        tag = request.GET.get('tag')
        if tag is not None:
            return redirect('posts:search-tag-view', tag=tag)

        q = request.GET.get('q')
        if q is not None:
            str_q = str(q)
            if len(str_q) > 4 and str_q[:4] == 'tag:':
                return redirect('posts:search-tag-view', tag=str(q)[4:])
            elif len(str_q) > 0:
                qs = []
                for question in Question.objects.all():
                    if str(question.text).find(str_q) != -1 or str(question.header).find(str_q) != -1:
                        qs.append(question)

                qs = sorted(qs, key=lambda item: (item.rating, item.created), reverse=True)

                page_num = request.GET.get('page')

                context = {
                    's_question': str_q,
                    'qs': Paginator(qs, 20).get_page(page_num),
                }
                return render(request, 'posts/search.html', context)

    return redirect('posts:main-post-view')


def search_tag_view(request, tag=None):
    qs = Question.objects.all()
    qs = [q for q in qs if tag in q.get_tag_list()]
    qs = sorted(qs, key=lambda item: (item.rating, item.created), reverse=True)
    page_num = request.GET.get('page')

    context = {
        'tag': tag,
        'qs': Paginator(qs, 20).get_page(page_num),
    }
    return render(request, 'posts/search.html', context)
