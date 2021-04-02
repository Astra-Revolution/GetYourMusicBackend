from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from GetYourMusic.consumers import ChatConsumer

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
