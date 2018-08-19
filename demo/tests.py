from django.test import TestCase

# Create your tests here.

class BaseBreadcrumbTestCase(TestCase):

    def setUp(self):
        from .models import TestModel
        self.crumbs = []
        self.instance = TestModel.objects.create(name='Test')

    def test_empty_crumbs(self):
        self.assertIsNotNone(self.instance)
        self.assertEqual(0, len(self.crumbs))
