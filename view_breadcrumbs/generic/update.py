from functools import partial

from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from .detail import DetailBreadcrumbMixin
from ..utils import action_view_name, classproperty


def _update_view_label(instance, format_string):
    return _(force_str(format_string) % {"instance": force_str(instance)})


class UpdateBreadcrumbMixin(DetailBreadcrumbMixin):
    # Home / object List / object / Update object
    update_format_str = _("Update: %(instance)s")

    @classproperty
    def update_view_name(self):
        return action_view_name(self.model, self.update_view_suffix, full=False)

    @property
    def __update_view_name(self):
        return action_view_name(self.model, self.update_view_suffix)

    def update_view_url(self, instance):
        return reverse(self.__update_view_name, kwargs={"pk": instance.pk})

    @property
    def crumbs(self):
        return super(UpdateBreadcrumbMixin, self).crumbs + [
            (
                partial(_update_view_label, format_string=self.update_format_str),
                self.update_view_url,
            ),
        ]
