"""
ASGI config for pronostico_clima project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pronostico_clima.settings')

application = get_asgi_application()
