from django.urls import reverse
from django.utils.html import format_html
from django_tables2 import Table

from demo.models import TestModel


class TestModelTable(Table):
    class Meta:
        model = TestModel
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name")

    def render_name(self, value, record):
        return format_html(
            "<a href={}>{}</b>",
            reverse("demo:testmodel_detail", kwargs={"pk": record.pk}),
            value,
        )
