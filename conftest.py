from django.conf import settings

def pytest_configure():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test.db',
            }
        },
        INSTALLED_APPS=[
            'django_bootstrap_breadcrumbs',
            'view_breadcrumbs',
        ],
    )
