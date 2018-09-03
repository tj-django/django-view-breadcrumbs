# django-view-breadcrumbs [![Build Status](https://travis-ci.org/jackton1/django-view-breadcrumbs.svg?branch=master)](https://travis-ci.org/jackton1/django-view-breadcrumbs) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6b447e364bef4988bda95bd0965bb4bc)](https://www.codacy.com/app/jackton1/django-view-breadcrumbs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jackton1/django-view-breadcrumbs&amp;utm_campaign=Badge_Grade) [![PyPI version](https://badge.fury.io/py/django-view-breadcrumbs.svg)](https://badge.fury.io/py/django-view-breadcrumbs)

This extends [django-bootstrap-breadcrumbs](http://django-bootstrap-breadcrumbs.readthedocs.io/en/latest/) providing generic breadcrumb mixin classes.

Replaces having to add ```{% breadcrumb $label $viewname [*args] [**kwargs] %}``` to every template.



Breadcrumb mixin classes provided.
----------------------------------

- `BaseBreadcrumbMixin`    - Base view requires a `crumbs` class property.
- `CreateBreadcrumbMixin`  - For create views `Home \ Posts \ Add Post`
- `DetailBreadcrumbMixin`  - For detail views `Home \ Posts \ Post 1`
- `ListBreadcrumbMixin`    - For list views `Home \ Posts`
- `UpdateBreadcrumbMixin`  - For Update views `Home \ Posts \ Post 1 \ Update Post 1`


## Installation:

```bash
$ pip install django-view-breadcrumbs

```

Add app to your INSTALLED_APPS

```python

INSTALLED_APPS = [
    ...
    'view-breadcrumbs',
    ...
]
```

## Usage:
`django-view-breadcrumbs` includes generic mixins that can be added to a class based view.

Using the generic breadcrumb mixin each breadcrumb will be added to the view dynamically
and can be overridden by providing a `crumbs` property.


### Sample crumbs:  `Home \ Posts \ Test - Post`

```python
from django.views.generic import DetailView
from django_view_breadcrumbs import DetailBreadcrumbMixin


class PostDetail(DetailBreadcrumbMixin, DetailView):
    model = Post
    template_name = 'app/post/detail.html'
```


In your `base.html` template simply add the ``render_breadcrumbs`` tag and any template
that inherits the base should have breadcrumbs included.
i.e  

In your ```base.html```

```jinja2
{% load django_bootstrap_breadcrumbs %}

{% block breadcrumbs %}
    {% render_breadcrumbs %}
{% endblock %}
```

And your ```create.html```.

```jinja2
{% extends 'base.html' %}
```


> All crumbs use the home root path `\` as the base this can be excluded by specifying `add_home = False`

### Sample crumbs: `Posts`

```python
from django.views.generic import ListView
from django_view_breadcrumbs import ListBreadcrumbMixin


class PostList(ListBreadcrumbMixin, ListView):
    model = Post
    template_name = 'app/post/list.html'
    add_home = False
```


> Can also override the view breadcrumb by specifying a list of tuples `[(Label, view path)]`.

### Custom crumbs: `Home \ My Test Breadcrumb`

URL conf.
```python
urlpatterns = [
   path('my-test-list-view/', views.TestView.as_view(), name='test_list_view'),
   path('my-test-detail-view/<int:pk>/', views.TestView.as_view(), name='test_detail_view'),
]
```

views.py

```python
from django.urls import reverse
from django.views.generic import ListView
from django_view_breadcrumbs import ListBreadcrumbMixin


class TestView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = 'app/test/test-list.html'
    crumbs = [('My Test Breadcrumb', reverse('test_list_view')]  # OR reverse_lazy
```

OR

```python
class TestView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = 'app/test/test-list.html'

    @cached_property
    def crumbs(self):
        return super(TestView, self).crumbs + [
            (self.object.name , reverse('test_detail_view', kwargs={'pk': self.object.pk})
        ]

```

