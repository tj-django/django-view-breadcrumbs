import os

from django import setup
from django.conf import settings

TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'demo', 'templates')

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
            'demo'
        ],
        ROOT_URLCONF='demo.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [TEST_DIR],
                'APP_DIRS': True,
            }
        ]
    )
    setup()
