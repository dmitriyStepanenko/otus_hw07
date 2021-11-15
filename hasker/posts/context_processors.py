from .models import Question


def trending(request):
    qs = Question.objects.all()

    trends = sorted(qs, key=lambda item: (item.rating, item.created), reverse=True)[:20]

    return {'trending_questions': trends}
