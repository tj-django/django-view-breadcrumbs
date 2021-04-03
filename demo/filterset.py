from django_filters import FilterSet

from demo.models import TestModel


class TestModelFilterSet(FilterSet):
    class Meta:
        model = TestModel
        fields = ['name', 'update_at']
