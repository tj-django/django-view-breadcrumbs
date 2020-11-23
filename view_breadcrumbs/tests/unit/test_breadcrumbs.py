from django.conf import settings
from django.test import TestCase, override_settings, RequestFactory
from django.utils.encoding import force_str
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from demo.models import TestModel
from demo.views import TestView
from view_breadcrumbs.generic import (
    BaseBreadcrumbMixin, ListBreadcrumbMixin, DetailBreadcrumbMixin,
    CreateBreadcrumbMixin, UpdateBreadcrumbMixin,
)
from view_breadcrumbs.templatetags.view_breadcrumbs import CONTEXT_KEY


class ActionTestMixin(object):
    @override_settings(BREADCRUMBS_HOME_LABEL='Custom Home')
    def test_custom_home_label(self):
        # TODO: Move this to use the default django client.
        instance = TestModel.objects.create(name='Test')

        TestViewClass = self.make_crumb_cls(
            'CustomView',
            (self.breadcrumb_mixin_cls, self.object_mixin, View),
            self.view_attrs,
        )
        v = TestViewClass()
        if isinstance(v, MultipleObjectMixin):
            v.object_list = v.get_queryset()
        else:
            v.kwargs = {'pk': instance.pk}
            v.object = v.get_object()

        v.get_context_data()

        labels = [
          force_str(paths[0])
          for paths in v.request.META[CONTEXT_KEY]
        ]

        self.assertEqual(settings.BREADCRUMBS_HOME_LABEL, 'Custom Home')
        self.assertIn('Custom Home', labels)


class BaseBreadcrumbTestCase(TestCase):
    breadcrumb_mixin_cls = BaseBreadcrumbMixin
    view_attrs = {}

    @classmethod
    def setUpTestData(cls):
        cls.crumbs = []

    @classmethod
    def make_crumb_cls(cls, class_name, bases, attrs):
        attrs['request'] = RequestFactory().request()
        return type(class_name, bases, attrs)

    def test_empty_crumbs(self):
        self.assertEqual(0, len(self.crumbs))

    def test_no_crumbs_property_raise_exception(self):
        TestViewClass = self.make_crumb_cls(
            'CustomView',
            (self.breadcrumb_mixin_cls, View),
            {**self.view_attrs, 'crumbs': BaseBreadcrumbMixin.crumbs},
        )

        with self.assertRaises(NotImplementedError) as exc:
            crumbs = TestViewClass().crumbs
            self.assertIsNone(crumbs)

        self.assertEqual(
            str(exc.exception),
            '{} should have a crumbs property.'.format(TestViewClass.__name__),
        )


    def test_custom_crumbs_property_is_valid(self):
        expected_crumbs = [('My Test Breadcrumb', '/')]

        TestViewClass = self.make_crumb_cls(
            'CustomView',
            (self.breadcrumb_mixin_cls, View),
            {'crumbs': expected_crumbs},
        )
        crumbs = TestViewClass().crumbs

        self.assertEqual(crumbs, expected_crumbs)

    def test_view_crumbs_is_valid(self):
        expected_crumbs = [('My Test Breadcrumb', 'test_view')]
        crumbs = TestView().crumbs

        self.assertEqual(crumbs, expected_crumbs)


class ListViewBreadcrumbTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = ListBreadcrumbMixin
    view_attrs = {'model': TestModel}
    object_mixin = MultipleObjectMixin


class DetailViewBreadcrumbTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = DetailBreadcrumbMixin
    view_attrs = {'model': TestModel}
    object_mixin = SingleObjectMixin

    @classmethod
    def setUpTestData(cls):
        cls.crumbs = []


class CreateBreadcrumbMixinTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = CreateBreadcrumbMixin
    view_attrs = {'model': TestModel}
    object_mixin = SingleObjectMixin

    @classmethod
    def setUpTestData(cls):
        cls.crumbs = []


class UpdateBreadcrumbMixinTestCase(ActionTestMixin, BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = UpdateBreadcrumbMixin
    view_attrs = {'model': TestModel}
    object_mixin = SingleObjectMixin

    @classmethod
    def setUpTestData(cls):
        cls.crumbs = []
