# coding: utf-8
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

SECRET_KEY = '_'
SITE_ID = 1
ROOT_URLCONF = 'test_app.urls'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'confirmanager',
    'test_app'
)
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
TEST_RUNNER = 'discover_runner.DiscoverRunner'