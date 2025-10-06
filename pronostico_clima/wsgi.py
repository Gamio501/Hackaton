"""
WSGI config for pronostico_clima project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pronostico_clima.settings')

application = get_wsgi_application()
