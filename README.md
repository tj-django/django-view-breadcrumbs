# django-view-breadcrumbs

This extends django-bootstrap-breadcrumbs providing generic breadcrumb mixin classes that will replace 
having to add the ```{% breadcrumb $label $viewname [*args] [**kwargs] %}``` to every template.


Using the breadcumb mixin the breadcrumbs are added for each view dynamically using the `model` and can be 
overridding by providing a `crumbs` property to the class. 


Usage:
```
from django.views.generic import DetailView
from django_view_breadcrumbs.generic import DetailBreadcrumbMixin

class PostDetail(DetailBreadcrumbMixin, DetailView):
    model = Post
    template_name = 'app/post/detail.html'
```
