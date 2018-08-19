import os
from setuptools import setup, find_packages

install_requires = [
    'Django>=1.11.10,<=2.0.2',
    'django-bootstrap-breadcrumbs==0.8.2',
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
}

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        yield f.read()


setup(
    name='django-view-breadcrumbs',
    python_requires='>=3.5',
    version='0.1.0',
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    long_description=read('README.md'),
    packages=find_packages(exclude=['demo', 'demo.migrations.*']),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Topics :: Django breadcrumbs',
    ],
    keywords=[
        'django breadcrumbs',
        'breadcrumbs',
        'django generic view breadcrumbs',
    ],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require=extras_require,
    url='https://github.com/jackton1/django-view-breadcrumbs',
    description='Django generic view breadcrumbs',
    zip_safe=False,
)


