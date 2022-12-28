import os

from setuptools import find_packages, setup

install_requires = [
    "Django",
    "six",
]

test_requires = [
    "tox",
    "tox-gh-actions",
    "coverage",
    "pytest",
    "pluggy>=0.7",
    "mock",
    "codacy-coverage",
]

doc_requires = [
    "Sphinx",
]

deploy_requires = [
    "bump2version",
    "readme_renderer[md]",
    "git-changelog",
    "twine",
]

local_dev_requires = [
    "pip-tools",
    "django_tables2",
    "django_bootstrap5",
    "django-filter",
]

extras_require = {
    "development": [
        local_dev_requires,
        install_requires,
        test_requires,
        doc_requires,
    ],
    "docs": doc_requires,
    "test": test_requires,
    "deploy": deploy_requires,
}

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, "README.md")

LONG_DESCRIPTION_TYPE = "text/markdown"
if os.path.isfile(README_PATH):
    with open(README_PATH) as f:
        LONG_DESCRIPTION = f.read()
else:
    LONG_DESCRIPTION = ""


setup(
    name="django-view-breadcrumbs",
    python_requires=">=3.6",
    version="2.4.1",
    author="Tonye Jack",
    author_email="jtonye@ymail.com",
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    packages=find_packages(exclude=["demo", "demo.migrations.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
    ],
    keywords=[
        "django breadcrumbs",
        "breadcrumbs",
        "django generic views breadcrumb",
    ],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require=extras_require,
    url="https://github.com/tj-django/django-view-breadcrumbs",
    description="Django generic view breadcrumbs",
    zip_safe=False,
)
