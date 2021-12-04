from django.conf import settings
from django.test import RequestFactory, TestCase, override_settings
from django.utils.encoding import force_str
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from demo.models import TestModel
from demo.views import TestView
from view_breadcrumbs import DeleteBreadcrumbMixin
from view_breadcrumbs.generic import (
    BaseBreadcrumbMixin,
    CreateBreadcrumbMixin,
    DetailBreadcrumbMixin,
    ListBreadcrumbMixin,
    UpdateBreadcrumbMixin,
)
from view_breadcrumbs.templatetags.view_breadcrumbs import CONTEXT_KEY


class BaseBreadcrumbTestCase(TestCase):
    breadcrumb_mixin_cls = BaseBreadcrumbMixin
    view_attrs = {}

    @classmethod
    def make_crumb_cls(cls, class_name, bases, attrs):
        attrs["request"] = RequestFactory().request()
        return type(class_name, bases, attrs)

    def test_no_crumbs_property_raise_exception(self):
        TestViewClass = self.make_crumb_cls(
            "CustomView",
            (self.breadcrumb_mixin_cls, View),
            {**self.view_attrs, "crumbs": BaseBreadcrumbMixin.crumbs},
        )

        with self.assertRaises(NotImplementedError) as exc:
            crumbs = TestViewClass().crumbs
            self.assertIsNone(crumbs)

        self.assertEqual(
            str(exc.exception),
            "{} should have a crumbs property.".format(TestViewClass.__name__),
        )

    def test_custom_crumbs_property_is_valid(self):
        expected_crumbs = [("My Test Breadcrumb", "/")]

        TestViewClass = self.make_crumb_cls(
            "CustomView",
            (self.breadcrumb_mixin_cls, View),
            {"crumbs": expected_crumbs},
        )
        crumbs = TestViewClass().crumbs

        self.assertEqual(crumbs, expected_crumbs)

    def test_view_crumbs_is_valid(self):
        expected_crumbs = [("My Test Breadcrumb", "test_view")]
        crumbs = TestView().crumbs

        self.assertEqual(crumbs, expected_crumbs)


class ActionTestMixin(object):
    object_mixin = None
    view_name = None

    def _get_view(self):
        # TODO: Move this to use the default django client.
        instance = TestModel.objects.create(name="Test")

        TestViewClass = self.make_crumb_cls(
            "CustomView",
            (self.breadcrumb_mixin_cls, self.object_mixin, View),
            self.view_attrs,
        )
        view = TestViewClass()
        if isinstance(view, MultipleObjectMixin):
            view.object_list = view.get_queryset()
        else:
            view.kwargs = {"pk": instance.pk}
            view.object = view.get_object()

        return view

    @override_settings(BREADCRUMBS_HOME_LABEL="Custom Home")
    def test_custom_home_label(self):
        view = self._get_view()
        view.get_context_data()

        labels = [force_str(paths[0]) for paths in view.request.META[CONTEXT_KEY]]

        self.assertEqual(settings.BREADCRUMBS_HOME_LABEL, "Custom Home")
        self.assertIn("Custom Home", labels)

    def test_valid_view_name(self):
        view = self._get_view()

        self.assertIsNotNone(getattr(view, "{}_view_name".format(self.view_name)))

    def test_valid_view_url(self):
        view = self._get_view()
        view_url = getattr(view, "{}_view_url".format(self.view_name))

        if isinstance(view_url, str):
            self.assertIsNotNone(view_url)
        else:
            self.assertIsNotNone(view_url(view.object))


class ListViewBreadcrumbTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = ListBreadcrumbMixin
    view_attrs = {"model": TestModel}
    object_mixin = MultipleObjectMixin
    view_name = "list"


class DetailViewBreadcrumbTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = DetailBreadcrumbMixin
    view_attrs = {"model": TestModel}
    object_mixin = SingleObjectMixin
    view_name = "detail"


class CreateBreadcrumbMixinTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = CreateBreadcrumbMixin
    view_attrs = {"model": TestModel}
    object_mixin = SingleObjectMixin
    view_name = "create"


class UpdateBreadcrumbMixinTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = UpdateBreadcrumbMixin
    view_attrs = {"model": TestModel}
    object_mixin = SingleObjectMixin
    view_name = "update"


class DeleteBreadcrumbMixinTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = DeleteBreadcrumbMixin
    view_attrs = {"model": TestModel}
    object_mixin = SingleObjectMixin
    view_name = "delete"
