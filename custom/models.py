from django.db import models
from django.utils.translation import gettext_lazy as _


class Library(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("library")
        verbose_name_plural = _("libraries")

    def __str__(self):
        return str(_(self.name))
