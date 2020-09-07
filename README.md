# django-view-breadcrumbs 

[![Build Status](https://travis-ci.org/tj-django/django-view-breadcrumbs.svg?branch=master)](https://travis-ci.org/tj-django/django-view-breadcrumbs) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6b447e364bef4988bda95bd0965bb4bc)](https://www.codacy.com/app/tj-django/django-view-breadcrumbs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tj-django/django-view-breadcrumbs&amp;utm_campaign=Badge_Grade) [![PyPI version](https://badge.fury.io/py/django-view-breadcrumbs.svg)](https://badge.fury.io/py/django-view-breadcrumbs) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section --> [![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

This provides a generic set of breadcrumb mixin classes.

Requires adding ```{% render_breadcrumbs %}``` to just the base template.

![Screenshot](./breadcrumbs.png)


In the `base.html` template simply add the ``render_breadcrumbs`` tag and any template
that inherits the base should have breadcrumbs included.
i.e  

```base.html```

```jinja2
{% load view_breadcrumbs %}

{% block breadcrumbs %}
    {% render_breadcrumbs %}
{% endblock %}
```

And your ```create.html```.

```jinja2
{% extends 'base.html' %}
```


Breadcrumb mixin classes provided.
----------------------------------

- `BaseBreadcrumbMixin`    - Base view requires a `crumbs` class property.
- `CreateBreadcrumbMixin`  - For create views `Home / Posts / Add Post`
- `DetailBreadcrumbMixin`  - For detail views `Home / Posts / Post 1`
- `ListBreadcrumbMixin`    - For list views `Home / Posts`
- `UpdateBreadcrumbMixin`  - For Update views `Home / Posts / Post 1 / Update Post 1`


## Installation:

```bash
$ pip install django-view-breadcrumbs

```

Add app to your INSTALLED_APPS

```python

INSTALLED_APPS = [
    ...,
    'view_breadcrumbs',
    ...,
]
```

## Usage:
`django-view-breadcrumbs` includes generic mixins that can be added to a class based view.

Using the generic breadcrumb mixin each breadcrumb will be added to the view dynamically
and can be overridden by providing a `crumbs` property.


### Settings:

To modify the root label site wide use

`BREADCRUMBS_HOME_LABEL` - Sets the root label (default: `Home`)


#### Example 

```python

BREADCRUMBS_HOME_LABEL = 'My new home'
```

Renders

![Screenshot](./custom-root-breadcrumb.png)


#### Sample crumbs:  `Home / Posts / Test - Post`

> NOTE: All url config should use a pattern `view_name=model_verbose_name_{action}` i.e `view_name=post_detail` for detail view. 

Actions include: 
 - "list" - `ListView`
 - "change" - `UpdateView`
 - "detail" - `DetailView`

In your `urls.py`
```python
  urlpatterns = [
      ...
      path('posts/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
      ...
  ]

```
`views.py`
```python
from django.views.generic import DetailView
from view_breadcrumbs import DetailBreadcrumbMixin


class PostDetail(DetailBreadcrumbMixin, DetailView):
    model = Post
    template_name = 'app/post/detail.html'
```

### Sample crumbs: `Posts`

> All crumbs use the home root path `/` as the base this can be excluded by specifying `add_home = False`

```python
from django.views.generic import ListView
from view_breadcrumbs import ListBreadcrumbMixin


class PostList(ListBreadcrumbMixin, ListView):
    model = Post
    template_name = 'app/post/list.html'
    add_home = False
```


> Can also override the view breadcrumb by specifying a list of tuples `[(Label, view path)]`.

### Custom crumbs: `Home / My Test Breadcrumb`

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
from view_breadcrumbs import ListBreadcrumbMixin
from demo.models import TestModel


class TestView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = 'app/test/test-list.html'
    crumbs = [('My Test Breadcrumb', reverse('test_list_view'))]  # OR reverse_lazy
```

OR

```python
from django.urls import reverse
from django.views.generic import ListView
from view_breadcrumbs import ListBreadcrumbMixin
from demo.models import TestModel
from django.utils.functional import cached_property


class TestView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = 'app/test/test-list.html'

    @cached_property
    def crumbs(self):
        return [('My Test Breadcrumb', reverse('test_list_view'))]

```

### Overriding the Home label for a specific view

```python
from django.utils.translation import gettext_lazy as _
from view_breadcrumbs import DetailBreadcrumbMixin
from django.views.generic import DetailView
from demo.models import TestModel


class TestDetailView(DetailBreadcrumbMixin, DetailView):
     model = TestModel
     home_label = _('My custom home')
     template_name = 'demo/test-detail.html'
```


> Refer to the demo app for more examples.

## Running locally

```bash
$ make migrate
$ make run
```

Spins up a django server running the demo app.

Visit `http://127.0.0.1:8090`

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://fansourcedpoisontour.com"><img src="https://avatars3.githubusercontent.com/u/1037197?v=4" width="100px;" alt=""/><br /><sub><b>Derek</b></sub></a><br /><a href="https://github.com/tj-django/django-view-breadcrumbs/commits?author=KrunchMuffin" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
