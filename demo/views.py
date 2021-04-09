from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django_tables2 import SingleTableMixin, MultiTableMixin
from django_filters.views import FilterView

from demo.filterset import TestModelFilterSet
from view_breadcrumbs import (
    BaseBreadcrumbMixin,
    CreateBreadcrumbMixin,
    DetailBreadcrumbMixin,
    ListBreadcrumbMixin,
    UpdateBreadcrumbMixin,
    DeleteBreadcrumbMixin,
)

from demo.models import TestModel
from demo.tables import TestModelTable
from view_breadcrumbs.generic.base import BaseModelBreadcrumbMixin
from view_breadcrumbs.templatetags.view_breadcrumbs import detail_instance_view_url


class TestHomeView(BaseBreadcrumbMixin, TemplateView):
    template_name = "demo/index.html"
    crumbs = []
    list_models = [TestModel]


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
