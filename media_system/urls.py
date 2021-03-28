from django.urls import path

from .views import genres_list, instruments_list

urlpatterns = [
    path('genres/', genres_list, name='genres_list'),
    path('instruments/', instruments_list, name='instruments_list'),
]