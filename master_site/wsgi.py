"""
WSGI config for master_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'master_site.settings')

application = get_wsgi_application()


'''
# For production only
import os
import sys

# Add your project path to the system path
path = '/home/earth696/master_site/Master_site'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'master_site.settings'

# Activate the virtual environment
VENV_PATH = '/home/yourusername/.virtualenvs/myproject-venv/bin/python'
if sys.version_info < (3, 6):
    raise Exception('PythonAnywhere supports Python 3.6 and above for this WSGI file.')

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

'''