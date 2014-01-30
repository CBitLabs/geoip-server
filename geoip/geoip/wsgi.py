"""
WSGI config for geoip project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geoip.settings")

if not settings.DEBUG:
    ROOT_DIR = os.environ.get("GEOIP_ROOT", "/home/ubuntu")

    sys.path.insert(0, '%s/geoip' % ROOT_DIR)

    # Add the site-packages of the chosen virtualenv to work with
    site.addsitedir(
        '%s/.virtualenvs/geoip/local/lib/python2.7/site-packages' % ROOT_DIR)

    # Activate your virtual env
    activate_env = os.path.expanduser(
        "%s/.virtualenvs/geoip/bin/activate_this.py" % ROOT_DIR)
    execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
