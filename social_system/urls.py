from django.urls import path

from .views import publication_list, musician_publications, publication_detail, list_comments_by_publication, \
    create_comments, comment_detail, list_notification_by_profile

urlpatterns = [
    path('publications/', publication_list, name='publication_list'),
    path('musicians/<int:musician_id>/publications/', musician_publications, name='musician_publications'),
    path('publications/<int:publication_id>/', publication_detail, name='publication_detail'),
    path('publications/<int:publication_id>/comments/', list_comments_by_publication,
         name='list_comments_by_publication'),
    path('publications/<int:publication_id>/commenters/<int:commenter_id>/comments/', create_comments,
         name='create_comments'),
    path('comments/<int:comment_id>/', comment_detail, name='comment_detail'),
    path('profiles/<int:profile_id>/notifications/', list_notification_by_profile,
         name='list_notification_by_profile')
]
