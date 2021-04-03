"""
ASGI config for GetYourMusic project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.layers import get_channel_layer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import GetYourMusic.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GetYourMusic.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            GetYourMusic.routing.websocket_urlpatterns
        )
    ),
})
