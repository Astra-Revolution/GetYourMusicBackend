from django.urls import path

from .views import genres_list, instruments_list, list_genres_by_musician, list_instruments_by_musician

urlpatterns = [
    path('genres/', genres_list, name='genres_list'),
    path('instruments/', instruments_list, name='instruments_list'),
    path('musicians/<int:musician_id>/genres/', list_genres_by_musician, name='list_genres_by_musician'),
    path('musicians/<int:musician_id>/instruments/', list_instruments_by_musician,
         name='list_instruments_by_musician'),
]