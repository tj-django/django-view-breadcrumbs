import os
from setuptools import setup, find_packages

install_requires = [
    'Django<=3.1.1',
]

test_requires = [
    'tox==3.20.0',
    'pytest==6.0.1',
    'pluggy>=0.7',
    'mock',
    'codacy-coverage==1.3.11',
]

doc_requires = [
    'Sphinx==3.2.1',
]

deploy_requires = [
    'bumpversion==0.6.0',
]

lint_requires = [
    'flake8==3.8.3',
    'yamllint==1.24.2',
    'isort',
]

local_dev_requires = [
    'pip-tools==5.3.1',
]

extras_require = {
    'development': [
        local_dev_requires,
        install_requires,
        test_requires,
        doc_requires,
        lint_requires,
    ],
    'docs': doc_requires,
    'test': test_requires,
    'lint': lint_requires,
    'deploy': deploy_requires,
}

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, 'README.md')

LONG_DESCRIPTION_TYPE = 'text/markdown'
if os.path.isfile(README_PATH):
    with open(README_PATH) as f:
        LONG_DESCRIPTION = f.read()
else:
    LONG_DESCRIPTION = ''

VERSION = (1, 0, 0)

version = '.'.join(map(str, VERSION))


setup(
    name='django-view-breadcrumbs',
    python_requires='>=3.5',
    version=version,
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    packages=find_packages(exclude=['demo', 'demo.migrations.*']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
    ],
    keywords=[
        'django breadcrumbs',
        'breadcrumbs',
        'django generic views breadcrumb',
    ],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require=extras_require,
    url='https://github.com/jackton1/django-view-breadcrumbs',
    description='Django generic view breadcrumbs',
    zip_safe=False,
)


