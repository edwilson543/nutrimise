"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# Standard library imports
import os

# Third party imports
from configurations import wsgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reciply.config.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Settings")

application = wsgi.get_wsgi_application()
