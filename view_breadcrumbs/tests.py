from django.test import TestCase

# Create your tests here.


class BaseBreadcrumbTestCase(TestCase):

    def setUp(self):
        self.crumbs = []

    def test_empty_crumbs(self):
        self.assertEqual(0, len(self.crumbs))
