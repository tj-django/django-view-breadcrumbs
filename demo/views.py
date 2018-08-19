from django.views.generic import ListView

from view_breadcrumbs import ListBreadcrumbMixin
from .models import TestModel


class TestView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = 'demo/test-list.html'
    crumbs = [('My Test Breadcrumb', 'test_view')]
