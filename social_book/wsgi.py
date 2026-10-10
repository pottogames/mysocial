"""
WSGI config for social_book project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_book.settings')

application = get_wsgi_application()

# Vercel serverless: the SQLite file in /tmp starts empty on every cold start, so create the tables.
# (With DATABASE_URL set, run `python manage.py migrate` against that database once instead.)
if os.environ.get('VERCEL') and not os.environ.get('DATABASE_URL'):
    from django.core.management import call_command
    call_command('migrate', interactive=False, verbosity=0)

# Vercel's Python runtime looks for a module-level `app`.
app = application
