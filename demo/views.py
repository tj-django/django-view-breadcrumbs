from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, SingleTableMixin

from custom.models import Library
from demo.filterset import TestModelFilterSet
from demo.models import TestModel
from demo.tables import TestModelTable
from view_breadcrumbs import (
    BaseBreadcrumbMixin,
    CreateBreadcrumbMixin,
    DeleteBreadcrumbMixin,
    DetailBreadcrumbMixin,
    ListBreadcrumbMixin,
    UpdateBreadcrumbMixin,
)
from view_breadcrumbs.generic.base import BaseModelBreadcrumbMixin
from view_breadcrumbs.templatetags.view_breadcrumbs import detail_instance_view_url


class TestHomeView(BaseBreadcrumbMixin, TemplateView):
    template_name = "demo/index.html"
    crumbs = []


class TestView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = "demo/test-custom.html"
    crumbs = [(_("My Test Breadcrumb"), "test_view")]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_paths"] = [
            (_("List tests"), reverse("demo:testmodel_list")),
        ]
        return context


class TestListsView(ListBreadcrumbMixin, ListView):
    model = TestModel
    template_name = "demo/test-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_paths = []

        for instance in self.object_list:
            view_paths.append(
                (
                    instance.name,
                    detail_instance_view_url(instance),
                ),
            )
        context["view_paths"] = view_paths
        return context


class TestCreateView(CreateBreadcrumbMixin, CreateView):
    model = TestModel
    template_name = "demo/test-create.html"
    fields = ["name"]

    def get_success_url(self) -> str:
        return self.list_view_url


class TestDetailView(DetailBreadcrumbMixin, DetailView):
    model = TestModel
    home_label = _("My new home")
    template_name = "demo/test-detail.html"


class TestUpdateView(UpdateBreadcrumbMixin, UpdateView):
    model = TestModel
    template_name = "demo/test-update.html"
    fields = ["name"]

    def get_success_url(self) -> str:
        return self.detail_view_url(self.object)


class TestDeleteView(DeleteBreadcrumbMixin, DeleteView):
    model = TestModel

    def get_success_url(self) -> str:
        return self.list_view_url


class LibraryListsView(ListBreadcrumbMixin, ListView):
    model = Library
    template_name = "demo/test-list.html"
    app_name = "demo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_paths = []

        for instance in self.object_list:
            view_paths.append(
                (
                    instance.name,
                    detail_instance_view_url(instance, app_name=self.app_name),
                ),
            )
        context["view_paths"] = view_paths
        return context


class LibraryDetailView(DetailBreadcrumbMixin, DetailView):
    model = Library
    home_label = _("My new home")
    app_name = "demo"
    template_name = "demo/test-detail.html"


class LibraryCreateView(CreateBreadcrumbMixin, CreateView):
    model = Library
    template_name = "demo/test-create.html"
    app_name = "demo"
    fields = ["name"]

    def get_success_url(self) -> str:
        return self.list_view_url


class LibraryUpdateView(UpdateBreadcrumbMixin, UpdateView):
    model = Library
    template_name = "demo/test-update.html"
    app_name = "demo"
    fields = ["name"]

    def get_success_url(self) -> str:
        return self.detail_view_url(self.object)


class LibraryDeleteView(DeleteBreadcrumbMixin, DeleteView):
    model = Library
    app_name = "demo"

    def get_success_url(self) -> str:
        return self.list_view_url


class TestModelSingleTableView(BaseModelBreadcrumbMixin, SingleTableMixin, FilterView):
    model = TestModel
    table_class = TestModelTable
    filterset_class = TestModelFilterSet
    template_name = "demo/test-table-list.html"

    @cached_property
    def crumbs(self):
        return [(self.model_name_title_plural, "/")]


class TestModelMultiTableView(BaseBreadcrumbMixin, MultiTableMixin, TemplateView):
    template_name = "demo/test-multi-table.html"
    tables = [
        TestModelTable(TestModel.objects.all()),
        TestModelTable(TestModel.objects.all(), exclude=("id",)),
    ]

    table_pagination = {"per_page": 10}

    @cached_property
    def crumbs(self):
        return [("Multi Tables", "/")]
