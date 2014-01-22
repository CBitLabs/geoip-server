import os
import sys
import site

sys.path.insert(0, '/home/jblum/geoip')

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/geoip/local/lib/python2.7/site-packages')


# Activate your virtual env
activate_env = os.path.expanduser("~/.virtualenvs/geoip/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from server import app as application