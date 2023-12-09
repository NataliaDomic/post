from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives
# from django.core.mail import send_mail
# from django.contrib.auth.models import Group
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/news">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        return user



        # send_mail(
        #     subject='Добро пожаловать на наш новостной портал!',
        #     message=f'{user.username}, вы успешно зарегистрировались!',
        #     from_email=None,
        #     recipient_list=[user.email],
        # )
        # return user



        # common_users = Group.objects.get(name="Authors")
        # user.groups.add(common_users)
        # return user

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )