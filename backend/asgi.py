"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from tweet import routes
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

http_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http" : http_application,
    "websocket" : AuthMiddlewareStack(URLRouter(routes.ws_patterns))
})