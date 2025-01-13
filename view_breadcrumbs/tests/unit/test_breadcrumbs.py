import inspect

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
        TestModel = self.view_attrs["model"]
        TestModel.get_absolute_url = lambda self: "test_model/%d" % self.pk

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

    def test_valid_view_label(self):
        view = self._get_view()
        view_label_name = "{}_view_label".format(self.view_name)
        view_label_func = getattr(view, view_label_name)

        kwargs = {}

        # check if it's a property and get the actual function
        if isinstance(view_label_func, property):
            view_label_func = view_label_func.fget

        # use inspect to get the function signature if callable
        if callable(view_label_func):
            signature = inspect.signature(view_label_func)
            if "instance" in signature.parameters:
                kwargs = {"instance": view.object}

        label = (
            view_label_func(**kwargs) if callable(view_label_func) else view_label_func
        )

        match self.view_name:
            case "list":
                self.assertEqual(label, view.model_name_title_plural)
            case "detail":
                self.assertEqual(
                    label, view.detail_format_string % force_str(view.object)
                )
            case "create":
                self.assertEqual(
                    label, view.add_format_string % {"model": view.model_name_title}
                )
            case "update":
                self.assertEqual(
                    label,
                    view.update_format_string % {"instance": force_str(view.object)},
                )
            case "delete":
                self.assertEqual(
                    label,
                    view.delete_format_string % {"instance": force_str(view.object)},
                )

        new_label = "TEST"

        @property
        def new_label_method(self, instance=None):
            return new_label

        # monkey patch view class method to override
        setattr(type(view), view_label_name, new_label_method)
        self.assertEqual(getattr(view, view_label_name), new_label)


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
