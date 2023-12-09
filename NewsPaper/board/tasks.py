from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from news.models import Post, Category
from news.signals import *
from celery import shared_task
import time

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def send_notifications(preview, pk, title, subscribers):...


@shared_task
def weekly_notification():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Посты за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()