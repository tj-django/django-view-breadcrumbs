# django-view-breadcrumbs

[![Test](https://github.com/tj-django/django-view-breadcrumbs/actions/workflows/test.yml/badge.svg)](https://github.com/tj-django/django-view-breadcrumbs/actions/workflows/test.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/537b0ce56e744f078f17cc8ccd4200d8)](https://www.codacy.com/gh/tj-django/django-view-breadcrumbs/dashboard?utm_source=github.com\&utm_medium=referral\&utm_content=tj-django/django-view-breadcrumbs\&utm_campaign=Badge_Grade) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tj-django/django-view-breadcrumbs/main.svg)](https://results.pre-commit.ci/latest/github/tj-django/django-view-breadcrumbs/main) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/537b0ce56e744f078f17cc8ccd4200d8)](https://www.codacy.com/gh/tj-django/django-view-breadcrumbs/dashboard?utm_source=github.com\&utm_medium=referral\&utm_content=tj-django/django-view-breadcrumbs\&utm_campaign=Badge_Coverage) [![PyPI version](https://badge.fury.io/py/django-view-breadcrumbs.svg)](https://badge.fury.io/py/django-view-breadcrumbs) [![Updates](https://pyup.io/repos/github/tj-django/django-view-breadcrumbs/shield.svg)](https://pyup.io/repos/github/tj-django/django-view-breadcrumbs/)

![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-view-breadcrumbs) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-view-breadcrumbs) [![Downloads](https://pepy.tech/badge/django-view-breadcrumbs)](https://pepy.tech/project/django-view-breadcrumbs)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Table of Contents

*   [Background](#background)
*   [Installation](#installation)
    *   [Add `view_breadcrumbs` to your INSTALLED\_APPS](#add-view_breadcrumbs-to-your-installed_apps)
*   [Breadcrumb mixin classes provided.](#breadcrumb-mixin-classes-provided)
*   [Settings](#settings)
    *   [Customization](#customization)
        *   [BREADCRUMBS\_TEMPLATE](#breadcrumbs_template)
            *   [Site wide](#site-wide)
            *   [Overriding the breadcrumb template for a single view](#overriding-the-breadcrumb-template-for-a-single-view)
        *   [BREADCRUMBS\_HOME\_LABEL](#breadcrumbs_home_label)
            *   [Site wide](#site-wide-1)
            *   [Overriding the Home label for a specific view](#overriding-the-home-label-for-a-specific-view)
*   [Translation support](#translation-support)
    *   [Example](#example)
*   [Usage](#usage)
    *   [View Configuration](#view-configuration)
        *   [django-tables-2](#django-tables-2)
    *   [URL Configuration](#url-configuration)
    *   [Examples](#examples)
        *   [Sample crumbs: `Posts`](#sample-crumbs-posts)
        *   [Sample crumbs:  `Home / Posts / Test - Post`](#sample-crumbs--home--posts--test---post)
        *   [Custom crumbs: `Home / My Test Breadcrumb`](#custom-crumbs-home--my-test-breadcrumb)
    *   [Using multiple apps](#using-multiple-apps)
*   [Running locally](#running-locally)
*   [Credits](#credits)
*   [Contributors ✨](#contributors-)

## Background

This package provides a set of breadcrumb mixin classes that can be added to any django class based view and requires adding just `{% render_breadcrumbs %}` to the base template.

<img width="1438" alt="breadcrumbs" src="https://user-images.githubusercontent.com/17484350/128493747-776706bf-d46c-4b57-ba54-c64fcc71ada7.png">

In the `base.html` template add the `render_breadcrumbs` tag and any template that inherits the base should have breadcrumbs included.

**Example:**

    my_app
       |--templates
                |--base.html
                |--create.html

`base.html`

```jinja2
{% load view_breadcrumbs %}

{% block breadcrumbs %}
    {% render_breadcrumbs %} {# Optionally provide a custom template e.g {% render_breadcrumbs "view_breadcrumbs/bootstrap5.html" %} #}
{% endblock %}
```

And your `create.html`.

```jinja2
{% extends "base.html" %}
```

## Installation

```bash
$ pip install django-view-breadcrumbs

```

### Add `view_breadcrumbs` to your INSTALLED\_APPS

```python

INSTALLED_APPS = [
    ...,
    "view_breadcrumbs",
    ...,
]
```

## Breadcrumb mixin classes provided.

*   `BaseBreadcrumbMixin`    - Subclasses requires a `crumbs` class property.
*   `CreateBreadcrumbMixin`  - For create views `Home / Posts / Add Post`
*   `DetailBreadcrumbMixin`  - For detail views `Home / Posts / Post 1`
*   `ListBreadcrumbMixin`    - For list views `Home / Posts`
*   `UpdateBreadcrumbMixin`  - For Update views `Home / Posts / Post 1 / Update Post 1`
*   `DeleteBreadcrumbMixin`  - For Delete views this has a link to the list view to be used as the success URL.

## Settings

> NOTE :warning:
>
> *   Make sure that `"django.template.context_processors.request"` is added to your TEMPLATE OPTIONS setting.

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
| `BREADCRUMBS_TEMPLATE`     | `"view_breadcrumbs/bootstrap5.html"`        |  Template used to render breadcrumbs.           |   [Predefined Templates](https://github.com/tj-django/django-view-breadcrumbs/tree/main/view_breadcrumbs/templates/view_breadcrumbs)                 |
| `BREADCRUMBS_HOME_LABEL`   |  `Home`                                     |  Default label for the root path  |         |

### Customization

#### BREADCRUMBS\_TEMPLATE

##### Site wide

```python
BREADCRUMBS_TEMPLATE = "my_app/breadcrumbs.html"
```

##### Overriding the breadcrumb template for a single view

Update the `base.html`

```jinja2
{% render_breadcrumbs "my_app/breadcrumbs.html" %}
```

#### BREADCRUMBS\_HOME\_LABEL

##### Site wide

```python
BREADCRUMBS_HOME_LABEL = "My new home"
```

##### Overriding the Home label for a specific view

```python
from django.utils.translation import gettext_lazy as _
from view_breadcrumbs import DetailBreadcrumbMixin
from django.views.generic import DetailView
from demo.models import TestModel


class TestDetailView(DetailBreadcrumbMixin, DetailView):
     model = TestModel
     home_label = _("My new home")
     template_name = "demo/test-detail.html"
```

*Renders*

<img width="436" alt="custom-root-breadcrumb" src="https://user-images.githubusercontent.com/17484350/128493798-c71a8071-e913-4875-80b6-c7b414ac4e24.png">

## [Translation support](https://docs.djangoproject.com/en/3.1/topics/i18n/translation/)

### Example

![translated-crumbs](https://user-images.githubusercontent.com/17484350/128493830-7e50a6a9-3648-48cb-b198-4646ee2b03cf.png)

## Usage

`django-view-breadcrumbs` includes generic mixins that can be added to a class based view.

Using the generic breadcrumb mixin each breadcrumb will be added to the view dynamically
and can be overridden by providing a `crumbs` property.

### View Configuration

> NOTE: :warning:
>
> *   Model based views should use a pattern `view_name=model_verbose_name_{action}`

|  Actions  |  View Class |  View name  | Sample Breadcrumb | Example  |
|-----------|-------------|-------------|-------------------|----------|
| `list`    | [`ListView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-display/#listview)  | `{model.verbose_name}_list` |  `Home / Posts`  |  |
| `create`  | [`CreateView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#createview) | `{model.verbose_name}_create` | `Home / Posts / Add Post` |  |
| `detail`  | [`DetailView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-display/#detailview) | `{model.verbose_name}_detail` | `Home / Posts / Test - Post` |  |
| `change`  | [`UpdateView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#updateview) | `{model.verbose_name}_update` | `Home / Posts / Test - Post / Update Test - Post` |  |
| `delete`  | [`DeleteView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#deleteview) | `{model.verbose_name}_delete` | N/A |
|   N/A     | [`TemplateView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/#templateview) | N/A  | N/A |  See: [Custom View](#custom-crumbs-home--my-test-breadcrumb) |
|   N/A     | [`FormView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#formview) | N/A  | N/A |  See: [Custom View](#custom-crumbs-home--my-test-breadcrumb) |
|   N/A     | [`AboutView`](https://docs.djangoproject.com/en/3.2/topics/class-based-views/#subclassing-generic-views) | N/A  | N/A |  See: [Custom View](#custom-crumbs-home--my-test-breadcrumb) |
|   N/A     | [`View`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/#view) | N/A  | N/A |  See: [Custom View](#custom-crumbs-home--my-test-breadcrumb) |

#### [django-tables-2](https://django-tables2.readthedocs.io/en/latest/index.html#)

|  Actions  |  View Class |  View name  | Sample Breadcrumb | Example  |
|-----------|-------------|-------------|-------------------|----------|
|   N/A     | [`SingleTableMixin`](https://django-tables2.readthedocs.io/en/latest/pages/generic-mixins.html?highlight=SingleTableMixin#a-single-table-using-singletablemixin) | N/A  | N/A |  See: [demo table view](https://github.com/tj-django/django-view-breadcrumbs/blob/main/demo/views.py#L154-L162) |
|   N/A     | [`MultiTableMixin`](https://django-tables2.readthedocs.io/en/latest/pages/generic-mixins.html?highlight=SingleTableMixin#multiple-tables-using-multitablemixin) | N/A  | N/A |  See: [demo table view](https://github.com/tj-django/django-view-breadcrumbs/blob/main/demo/views.py#L166-L173) |
|   N/A     | [`SingleTableView`](https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html?highlight=SingleTableView#singletableview) | N/A  | N/A |  Same implementation as `SingleTableMixin` |

For more examples see: [demo app](https://github.com/tj-django/django-view-breadcrumbs/tree/main/demo)

### URL Configuration

Based on the table of actions listed above there's a strict `view_name` requirement that needs to be adhered to in order for breadcrumbs to work.

This can be manually entered in your `urls.py` or you can optionally use the following class properties instead of hardcoding the `view_name`.

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

### Examples

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

**OR**

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

> Refer to the [demo app](https://github.com/tj-django/django-view-breadcrumbs/tree/main/demo) for more examples.

### Using multiple apps

To reference models from a different application you need to override the `app_name` class attribute.

Example:
Using a `Library` model that is imported from a `custom` application that you want to render in a `demo` app view.

```python
INSTALLED_APPS =  [
    ...
    "demo",
    "custom",
    ...
]
```

`demo/views.py`

```python
class LibraryDetailView(DetailBreadcrumbMixin, DetailView):
    model = Library
    app_name = "demo"
    ...
```

## Running locally

```bash
$ git clone git@github.com:tj-django/django-view-breadcrumbs.git
$ make install-dev
$ make migrate
$ make run
```

Spins up a django server running the demo app.

Visit `http://127.0.0.1:8090`

## Credits

*   [django-bootstrap-breadcrumbs](https://github.com/prymitive/bootstrap-breadcrumbs)

To file a bug or submit a patch, please head over to [django-view-breadcrumbs on github](https://github.com/tj-django/django-view-breadcrumbs/issues).

If you feel generous and want to show some extra appreciation:

Support me with a :star:

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

[buymeacoffee]: https://www.buymeacoffee.com/jackton1

[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->

<!-- prettier-ignore-start -->

<!-- markdownlint-disable -->

<table>
  <tr>
    <td align="center"><a href="https://fansourcedpoisontour.com"><img src="https://avatars3.githubusercontent.com/u/1037197?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Derek</b></sub></a><br /><a href="https://github.com/tj-django/django-view-breadcrumbs/commits?author=KrunchMuffin" title="Documentation">📖</a></td>
    <td align="center"><a href="http://www.emencia.com"><img src="https://avatars.githubusercontent.com/u/1572165?v=4?s=100" width="100px;" alt=""/><br /><sub><b>David THENON</b></sub></a><br /><a href="https://github.com/tj-django/django-view-breadcrumbs/commits?author=sveetch" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->

<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
