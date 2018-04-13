# minimal django settings required to build documentation
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

SECRET_KEY = 'f$J4FB3B=}1bFtJ$}b9s28Vsf?&otV}o0*V)g;#OD5%20uksel'

