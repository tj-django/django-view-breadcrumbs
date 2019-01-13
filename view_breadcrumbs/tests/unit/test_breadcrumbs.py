from django.test import TestCase
from django.views.generic.base import View

from demo.models import TestModel
from demo.views import TestView
from view_breadcrumbs.generic import (
    BaseBreadcrumbMixin, ListBreadcrumbMixin, DetailBreadcrumbMixin,
    CreateBreadcrumbMixin, UpdateBreadcrumbMixin,
)


class BaseBreadcrumbTestCase(TestCase):
    breadcrumb_mixin_cls = BaseBreadcrumbMixin
    view_attrs = {}

    @classmethod
    def setUpTestData(cls):
        cls.crumbs = []
        cls.instance = TestModel.objects.create(name='Test')

    @classmethod
    def make_crumb_cls(cls, class_name, bases, attrs):
        return type(class_name, bases, attrs)

    def test_empty_crumbs(self):
        self.assertIsNotNone(self.instance)
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


class ListViewBreadcrumbTestCase(BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = ListBreadcrumbMixin
    view_attrs = {'model': TestModel}


class DetailViewBreadcrumbTestCase(BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = DetailBreadcrumbMixin
    view_attrs = {'model': TestModel}

    @classmethod
    def setUpTestData(cls):
        cls.crumbs = []


class CreateBreadcrumbMixinTestCase(BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = CreateBreadcrumbMixin
    view_attrs = {'model': TestModel}

    @classmethod
    def setUpTestData(cls):
        cls.crumbs = []


class UpdateBreadcrumbMixinTestCase(BaseBreadcrumbTestCase):
    breadcrumb_mixin_cls = UpdateBreadcrumbMixin
    view_attrs = {'model': TestModel}

    @classmethod
    def setUpTestData(cls):
        cls.crumbs = []



