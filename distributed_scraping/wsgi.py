#-*- coding: utf-8 -*-

"""
WSGI config for distributed_scraping project.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "distributed_scraping.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

