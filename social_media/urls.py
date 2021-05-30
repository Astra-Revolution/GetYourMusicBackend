from django.urls import path

from .views import publication_list, musician_publications, publication_detail, list_comments_by_publication, \
    create_comments, comment_detail, list_notification_by_profile, list_followed_by_musician, \
    list_follower_by_musician, create_delete_following, genres_list, instruments_list, list_genres_by_musician, \
    list_instruments_by_musician, musicians_genres, musicians_instruments

urlpatterns = [
    path('genres/', genres_list, name='genres_list'),
    path('instruments/', instruments_list, name='instruments_list'),
    path('musicians/<int:musician_id>/genres/', list_genres_by_musician, name='list_genres_by_musician'),
    path('musicians/<int:musician_id>/instruments/', list_instruments_by_musician,
         name='list_instruments_by_musician'),
    path('genres/<genre_id>/musicians/<int:musician_id>/', musicians_genres, name='musicians_genres'),
    path('instruments/<instrument_id>/musicians/<int:musician_id>/', musicians_instruments,
         name='musicians_instruments'),
    path('publications/', publication_list, name='publication_list'),
    path('musicians/<int:musician_id>/publications/', musician_publications, name='musician_publications'),
    path('publications/<int:publication_id>/', publication_detail, name='publication_detail'),
    path('publications/<int:publication_id>/comments/', list_comments_by_publication,
         name='list_comments_by_publication'),
    path('publications/<int:publication_id>/commenters/<int:commenter_id>/comments/', create_comments,
         name='create_comments'),
    path('comments/<int:comment_id>/', comment_detail, name='comment_detail'),
    path('followers/<int:musician_id>/followed/', list_followed_by_musician, name='list_followed_by_musician'),
    path('followed/<int:musician_id>/follower/', list_follower_by_musician, name='list_follower_by_musician'),
    path('followers/<int:follower_id>/followed/<int:followed_id>/following', create_delete_following,
         name='create_delete_following'),
    path('profiles/<int:profile_id>/notifications/', list_notification_by_profile,
         name='list_notification_by_profile'),
]
