"""
ASGI config for Projet project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from Admin import routing as Admin_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projet.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        Admin_routing.websocket_urlpatterns
    ),
})
