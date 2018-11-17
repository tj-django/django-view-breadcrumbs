import os
from setuptools import setup, find_packages

install_requires = [
    'Django>=1.11.10,>=2.0.2,<3.0',
    'django-bootstrap-breadcrumbs==0.9.1',
]

test_requires = [
    'tox==2.9.1',
    'pytest==3.7.2',
    'pluggy>=0.7',
    'mock==2.0.0',
    'codacy-coverage==1.3.10',
]

doc_requires = [
    'Sphinx==1.6.5',
]

deploy_requires = [
    'bumpversion==0.5.3',
]

lint_requires = [
    'flake8==3.4.1',
    'yamllint==1.10.0',
    'isort==4.2.15',
]

local_dev_requires = [
    'pip-tools==2.0.2',
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

VERSION = (0, 0, 7)

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
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
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


