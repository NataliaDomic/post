from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import datetime
from django.utils import timezone
from .models import Post, Category
from django.contrib.auth.models import User


@shared_task
def post_created(id):
    instance = Post.objects.get(id=id)

    subscribers = []

    for category in instance.postCategory.all():
        subscribers += User.objects.filter(
            subscriptions__category=category).values_list('email', flat=True)

    subject = f'New post at your favourite category {instance.postCategory}'

    text_content = (
        f'Title: {instance.title}\n'
        f'Text: {instance.text}\n\n'
        f'Click on link: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    html_content = (
        f'Title: {instance.title}<br>'
        f'Text: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Click on link</a>'
    )

    for email in subscribers:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_send_emails():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscriptions = (Category.objects.filter(name__in=categories).values_list('subscriptions__user__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='News per week',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriptions,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()