import os
import sys
import site

ROOT_DIR = os.environ.get("GEOIP_ROOT", "/home/jblum")

sys.path.insert(0, '%s/geoip' % ROOT_DIR)

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('%s/.virtualenvs/geoip/local/lib/python2.7/site-packages' % ROOT_DIR)


# Activate your virtual env
activate_env = os.path.expanduser("%s/.virtualenvs/geoip/bin/activate_this.py" % ROOT_DIR)
execfile(activate_env, dict(__file__=activate_env))

from server import app as application