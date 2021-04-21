from django.conf.urls import url

from messaging.consumers import ChatConsumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_code>\w+)$', ChatConsumer.as_asgi())
]

# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
