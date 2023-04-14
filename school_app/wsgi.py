"""
WSGI config for school_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/var/www/schoobees')

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/schoobees')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schoobees.school_app.settings")

application = get_wsgi_application()
