from django.conf.urls import url

from messaging.consumers import ChatConsumer

channel_routing = [
    url(r'^ws/chat/(?P<room_code>\w+)$', ChatConsumer.as_asgi())
]
