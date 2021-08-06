from django.db import models
from django.utils.translation import gettext_lazy as _
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class Library(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("library")
        verbose_name_plural = _("libraries")

    def __str__(self):
        return str(_(self.name))
