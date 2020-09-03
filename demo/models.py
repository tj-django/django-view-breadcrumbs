from django.db import models
from django.utils.translation import gettext_noop as _
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class TestModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return _(self.name)

    __repr__ = __str__

