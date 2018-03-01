# django-view-breadcrumbs [![Build Status](https://travis-ci.org/jackton1/django-view-breadcrumbs.svg?branch=master)](https://travis-ci.org/jackton1/django-view-breadcrumbs)[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6b447e364bef4988bda95bd0965bb4bc)](https://www.codacy.com/app/jackton1/django-view-breadcrumbs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jackton1/django-view-breadcrumbs&amp;utm_campaign=Badge_Grade)

This extends [django-bootstrap-breadcrumbs](http://django-bootstrap-breadcrumbs.readthedocs.io/en/latest/) providing generic breadcrumb mixin classes.

This will replace having to add ```{% breadcrumb $label $viewname [*args] [**kwargs] %}``` to every template.


Using the generic breadcumb mixin each page breadcrumbs are added for each view dynamically using the `model` and can be 
overridding by providing a `crumbs` property to the class. 


Usage:
```python
from django.views.generic import DetailView
from django_view_breadcrumbs.generic import DetailBreadcrumbMixin

class PostDetail(DetailBreadcrumbMixin, DetailView):
    model = Post
    template_name = 'app/post/detail.html'
```
