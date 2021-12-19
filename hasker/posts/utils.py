from django.core.mail import send_mail
from django.conf import settings


def send_email(question, profile):
    subject = 'New answer'
    message = f'There is new answer to your question "{question.header}" from "{profile.username}".\n' \
              f'Link to your question: {question.get_absolute_url()}.\n' \
              f'This mail was send automatically please do not answer this mail'
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[str(question.author.email)],
        fail_silently=True
    )


def change_rating(user, main_list, coupling_list):
    if user in main_list.all():
        main_list.remove(user)
    else:
        main_list.add(user)
        if user in coupling_list.all():
            coupling_list.remove(user)
