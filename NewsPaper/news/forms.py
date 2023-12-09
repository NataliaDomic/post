from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
       model = Post
       fields = [
           'author',
           'categoryType',
           'category',
           'title',
           'text',
       ]

        # labels = {
        #     'author': 'Автор',
        #     'categoryType': 'Тип',
        #     'postCategory': 'Категория',
        #     'title': 'Название',
        #     'text': 'Текст',
        # }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Содержание не должно быть идентично заголовку."
            )

        return cleaned_data