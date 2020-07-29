import os

from django.conf import settings
import pytest


@pytest.fixture(scope="session")
def django_db_setup():
    """
    It sets up the existing database for the connection
    :return:
    """
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('PG_DBNAME'),
            'USER': os.getenv('PG_DB_USER'),
            'PASSWORD': os.getenv('PG_DB_PASSWORD'),
            'HOST': os.getenv('PG_DB_HOST'),
            'PORT': os.getenv('PG_DB_PORT')
        }
    }


@pytest.fixture
def db_access_without_rollback_and_truncate(request, django_db_setup, django_db_blocker):
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)
