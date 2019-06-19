from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin
from .models import TestModel


class TestView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = 'demo/test-custom.html'
    crumbs = [('My Test Breadcrumb', 'test_view')]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_paths'] = [
            ('List tests', reverse('demo:testmodel_list')),
        ]
        return context


class TestListsView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = 'demo/test-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_paths = []

        for test in self.object_list:
            view_paths.append(
                (test.name, reverse('demo:testmodel_detail', kwargs={'pk': test.pk})),
            )
        context['view_paths'] = view_paths
        return context


class TestDetailView(DetailBreadcrumbMixin, DetailView):
    model = TestModel
    home_label = _('My new home')
    template_name = 'demo/test-detail.html'
