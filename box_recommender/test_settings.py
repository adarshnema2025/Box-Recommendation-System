"""
Optional settings override so tests can run against SQLite without needing
a running Postgres instance. Usage:

    python manage.py test --settings=box_recommender.test_settings
"""
from .settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}