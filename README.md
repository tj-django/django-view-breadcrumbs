# django-view-breadcrumbs 

[![Build Status](https://travis-ci.org/tj-django/django-view-breadcrumbs.svg?branch=master)](https://travis-ci.org/tj-django/django-view-breadcrumbs) ![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-view-breadcrumbs) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-view-breadcrumbs) [![Downloads](https://pepy.tech/badge/django-view-breadcrumbs)](https://pepy.tech/project/django-view-breadcrumbs)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6b447e364bef4988bda95bd0965bb4bc)](https://www.codacy.com/app/tj-django/django-view-breadcrumbs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tj-django/django-view-breadcrumbs&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/537b0ce56e744f078f17cc8ccd4200d8)](https://www.codacy.com/gh/tj-django/django-view-breadcrumbs/dashboard?utm_source=github.com&utm_medium=referral&utm_content=tj-django/django-view-breadcrumbs&utm_campaign=Badge_Coverage) [![PyPI version](https://badge.fury.io/py/django-view-breadcrumbs.svg)](https://badge.fury.io/py/django-view-breadcrumbs) [![Updates](https://pyup.io/repos/github/tj-django/django-view-breadcrumbs/shield.svg)](https://pyup.io/repos/github/tj-django/django-view-breadcrumbs/)  <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section --> [![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-) 
<!-- ALL-CONTRIBUTORS-BADGE:END -->


Provides a generic set of breadcrumb mixin classes.

Requires adding ```{% render_breadcrumbs %}``` to just the base template.

![Screenshot](./breadcrumbs.png)


In the `base.html` template simply add the ``render_breadcrumbs`` tag and any template
that inherits the base should have breadcrumbs included.
i.e  

```base.html```

```jinja2
{% load view_breadcrumbs %}

{% block breadcrumbs %}
    {% render_breadcrumbs %} {# Optionally provide a template e.g {% render_breadcrumbs "view_breadcrumbs/bootstrap5.html" %} #}
{% endblock %}
```

And your ```create.html```.

```jinja2
{% extends "base.html" %}
```


Breadcrumb mixin classes provided.
----------------------------------

- `BaseBreadcrumbMixin`    - Base view requires a `crumbs` class property.
- `CreateBreadcrumbMixin`  - For create views `Home / Posts / Add Post`
- `DetailBreadcrumbMixin`  - For detail views `Home / Posts / Post 1`
- `ListBreadcrumbMixin`    - For list views `Home / Posts`
- `UpdateBreadcrumbMixin`  - For Update views `Home / Posts / Post 1 / Update Post 1`
- `DeleteBreadcrumbMixin`  - For Delete views this has a link to the list view to be used as the success URL.


## Installation

```bash
$ pip install django-view-breadcrumbs

```

### Add `view_breadcrumbs` to your INSTALLED_APPS

```python

INSTALLED_APPS = [
    ...,
    "view_breadcrumbs",
    ...,
]
```


## Settings

> NOTE :warning:
> * Make sure that `"django.template.context_processors.request"` is added to your TEMPLATE OPTIONS setting.

```python
TEMPLATES  = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request", # <- This context processor is required
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

Modify the defaults using the following:

| Name                       | Default                                     | Description |    Options          |
|----------------------------|---------------------------------------------|-------------|---------------------|
| `BREADCRUMBS_TEMPLATE`     | `"view_breadcrumbs/bootstrap4.html"`        |  Template used to render breadcrumbs.           |   [Predefined Templates](https://github.com/tj-django/django-view-breadcrumbs/tree/master/view_breadcrumbs/templates/view_breadcrumbs)                 |
| `BREADCRUMBS_HOME_LABEL`   |  `Home`                                     |  Default label for the root path  |         |


To modify the root label site wide use

`BREADCRUMBS_HOME_LABEL` - Sets the root label (default: `Home`)


### Example 

```python

BREADCRUMBS_HOME_LABEL = "My new home"
```

*Renders*

![Screenshot](./custom-root-breadcrumb.png)


*Using django's [translation](https://docs.djangoproject.com/en/3.1/topics/i18n/translation/) support*

![Translated Screenshot](./translated-crumbs.png)


## Usage
`django-view-breadcrumbs` includes generic mixins that can be added to a class based view.

Using the generic breadcrumb mixin each breadcrumb will be added to the view dynamically
and can be overridden by providing a `crumbs` property.


### View Configuration

> NOTE: :warning:
> * Model based views should use a pattern `view_name=model_verbose_name_{action}`  


|  Actions  |  View Class |  View name  | Sample Breadcrumb |
|-----------|-------------|-------------|-------------------| 
| `list`    | `ListView`  | `{model.verbose_name}_list` |  `Home / Posts`  |
| `create`  | `CreateView`| `{model.verbose_name}_create` | `Home / Posts / Add Post` |
| `detail`  | `DetailView`| `{model.verbose_name}_detail` | `Home / Posts / Test - Post` |
| `change`  | `UpdateView`| `{model.verbose_name}_update` | `Home / Posts / Test - Post / Update Test - Post` |
| `delete`  | `DeleteView`| `{model.verbose_name}_delete` | N/A |

For views classes like: `TemplateView` | `AboutView` | `View`

> See: [Custom View](#custom-crumbs-home--my-test-breadcrumb)

For usage with [django tables 2](https://django-tables2.readthedocs.io/en/latest/index.html#)

> See: [demo](https://github.com/tj-django/django-view-breadcrumbs/blob/update-readme-to-highlight-usage-of-custom-views/demo/views.py#L100)

Optionally this can use the following class properties instead of hardcoding the view names.

```python
...
    path("tests/", TestListsView.as_view(), name=TestListsView.list_view_name),
    path(
        "tests/<slug:slug>/", 
        TestDetailView.as_view(),
        name=TestDetailView.detail_view_name,
    ),
    path(
        "tests/<slug:slug>/update/",
        TestUpdateView.as_view(),
        name=TestUpdateView.update_view_name,
    ),
    path(
        "tests/<slug:slug>/delete/",
        TestDeleteView.as_view(),
        name=TestDeleteView.delete_view_name,
    ),
...
```

For more examples see: [demo app](https://github.com/tj-django/django-view-breadcrumbs/tree/master/demo)


#### Sample crumbs:  `Home / Posts / Test - Post`

In your `urls.py`
```python
  urlpatterns = [
      ...
      path("posts/<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
      ...
      # OR
      ...
      path("posts/<slug:slug>/", views.PostDetail.as_view(), name=views.PostDetail.detail_view_name),
      ...
  ]

```
`views.py`
```python
from django.views.generic import DetailView
from view_breadcrumbs import DetailBreadcrumbMixin


class PostDetail(DetailBreadcrumbMixin, DetailView):
    model = Post
    template_name = "app/post/detail.html"
    breadcrumb_use_pk = False
```

#### Sample crumbs: `Posts`

In your urls.py
```python
  urlpatterns = [
      ...
      path("posts/", views.PostList.as_view(), name="post_list"),
      ...
      # OR
      ...
      path("posts/", views.PostList.as_view(), name=views.PostList.list_view_name),
      ...
  ]
```

> All crumbs use the home root path `/` as the base this can be excluded by specifying `add_home = False`

```python
from django.views.generic import ListView
from view_breadcrumbs import ListBreadcrumbMixin


class PostList(ListBreadcrumbMixin, ListView):
    model = Post
    template_name = "app/post/list.html"
    add_home = False
```


#### Custom crumbs: `Home / My Test Breadcrumb`

URL configuration.

```python
    urlpatterns = [
       path("my-custom-view/", views.CustomView.as_view(), name="custom_view"),
    ]
```

views.py

```python
from django.urls import reverse
from django.views.generic import View
from view_breadcrumbs import BaseBreadcrumbMixin
from demo.models import TestModel


class CustomView(BaseBreadcrumbMixin, View):
    model = TestModel
    template_name = "app/test/custom.html"
    crumbs = [("My Test Breadcrumb", reverse("custom_view"))]  # OR reverse_lazy
```

OR

```python
from django.urls import reverse
from django.views.generic import View
from view_breadcrumbs import BaseBreadcrumbMixin
from demo.models import TestModel
from django.utils.functional import cached_property


class CustomView(BaseBreadcrumbMixin, View):
    template_name = "app/test/custom.html"

    @cached_property
    def crumbs(self):
        return [("My Test Breadcrumb", reverse("custom_view"))]

```

### Overriding the Home label for a specific view

```python
from django.utils.translation import gettext_lazy as _
from view_breadcrumbs import DetailBreadcrumbMixin
from django.views.generic import DetailView
from demo.models import TestModel


class TestDetailView(DetailBreadcrumbMixin, DetailView):
     model = TestModel
     home_label = _("My custom home")
     template_name = "demo/test-detail.html"
```

> Refer to the [demo app](https://github.com/tj-django/django-view-breadcrumbs/tree/master/demo) for more examples.

## Running locally

```bash
$ make install-dev
$ make migrate
$ make run
```

Spins up a django server running the demo app.

Visit `http://127.0.0.1:8090`

## Credits
- [django-bootstrap-breadcrumbs](https://github.com/prymitive/bootstrap-breadcrumbs)


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
