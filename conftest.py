import os
import sys

from django import setup
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(BASE_DIR, "demo", "templates")


def pytest_configure(debug=False):
    base_settings = dict(
        DEBUG=debug,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "test.db",
            }
        },
        INSTALLED_APPS=["view_breadcrumbs", "demo"],
        ROOT_URLCONF="demo.urls",
        USE_I18N=True,
        USE_L10N=True,
        # Provide a lists of languages which your site supports.
        LANGUAGES=(
            ("en", _("English")),
            ("fr", _("French")),
        ),
        # Set the default language for your site.
        LANGUAGE_CODE="en",
        # Tell Django where the project's translation files should be.
        LOCALE_PATHS=(os.path.join(BASE_DIR, "locale"),),
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [TEST_DIR],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ],
    )

    if debug:
        base_settings.update(
            {
                "ALLOWED_HOSTS": ["127.0.0.1", "localhost"],
                "INSTALLED_APPS": [
                    "django.contrib.auth",
                    "django.contrib.contenttypes",
                    "django.contrib.sessions",
                    "view_breadcrumbs",
                    "demo",
                ],
            }
        )
    settings.configure(**base_settings)
    setup()
    if not debug:
        create_db()


def create_db():
    if sys.version_info > (3, 5):
        from django.db import connection

        with connection.cursor() as c:
            c.executescript(
                """
            BEGIN;
            --
            -- Create model TestModel
            --
            DROP TABLE  IF EXISTS "demo_testmodel";
            CREATE TABLE "demo_testmodel" (
                "created_at" datetime NOT NULL,
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "update_at" datetime NOT NULL,
                "name" varchar(50) NOT NULL
            );
            COMMIT;
            """
            )
