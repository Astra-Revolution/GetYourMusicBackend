from django.urls import path

from messaging.views import list_chats_by_user

urlpatterns = [
    path('profiles/<int:user_id>/chats/', list_chats_by_user, name='list_chats_by_user'),
]