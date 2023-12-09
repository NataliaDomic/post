from django.urls import path
from .views import (NewsList, NewDetail, PostCreate, PostUpdate, PostDelete, subscriptions)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', NewsList.as_view(), name='post_list'),
    path('<int:pk>', cache_page(60*10)(NewDetail.as_view()), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]