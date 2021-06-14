

from django.urls import path

from messaging.views import *

urlpatterns = [
    path('profiles/<int:user_id>/chats/', list_chats_by_user, name='list_chats_by_user'),
    path('profiles/<int:user_id>/receivers/<int:receiver_id>/chats/', chat_detail, name='chat_detail'),
]

# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
