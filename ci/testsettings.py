# minimal django settings required to run django-dependent tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test.db",
    }
}

INSTALLED_APPS = (
    # 'django.contrib.contenttypes',
    'dal',
    'dal_select2',
    'viapy',
)

ROOT_URLCONF = 'viapy.test_urls'

LANGUAGE_CODE = 'en-us'

# must be added
# SECRET_KEY = ''

