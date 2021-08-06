from functools import partial

from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from ..utils import action_view_name, classproperty
from .detail import DetailBreadcrumbMixin


def _update_view_label(instance, format_string):
    return _(force_str(format_string) % {"instance": force_str(instance)})


class UpdateBreadcrumbMixin(DetailBreadcrumbMixin):
    # Home / object List / object / Update object
    update_format_str = _("Update: %(instance)s")

    @classproperty
    def update_view_name(self):
        return action_view_name(
            model=self.model,
            action=self.update_view_suffix,
            app_name=self.app_name,
            full=False,
        )

    @property
    def __update_view_name(self):
        return action_view_name(
            model=self.model, action=self.update_view_suffix, app_name=self.app_name
        )

    def update_view_url(self, instance):
        if self.breadcrumb_use_pk:
            return reverse(
                self.__update_view_name, kwargs={self.pk_url_kwarg: instance.pk}
            )

        return reverse(
            self.__update_view_name,
            kwargs={self.slug_url_kwarg: getattr(instance, self.slug_field)},
        )

    @property
    def crumbs(self):
        return super(UpdateBreadcrumbMixin, self).crumbs + [
            (
                partial(_update_view_label, format_string=self.update_format_str),
                self.update_view_url,
            ),
        ]
