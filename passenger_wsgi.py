# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/o/o1233239/gosuclygi.site/PytonSite')
sys.path.insert(1, '/home/o/o1233239/.local/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'PytonSite.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()