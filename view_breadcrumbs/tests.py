from django.test import TestCase


class BreadcrumbTestCase(TestCase):

    def setUp(self):
        self.crumbs = []

    def test_empty_crumbs(self):
        self.assertEqual(0, len(self.crumbs))
