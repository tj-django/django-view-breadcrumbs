from setuptools import setup, find_packages

install_requires = [
    'Django>=1.11.10<=2.0.2',
    'django-bootstrap-breadcrumbs==0.8.2',
]

test_requires = [
    'tox==2.9.1',
    'pytest==3.4.1',
    'mock==2.0.0',
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
    'pip-tools==1.11.0',
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
}


setup(
    name='django_view_breadcrumbs',
    version='0.0.1',
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require=extras_require,
    url='https://github.com/jackton1/django-view-breadcrumbs',
    description='Django View Breadcrumbs',
    zip_safe=False,
)


