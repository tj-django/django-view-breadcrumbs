from functools import partial

from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from ..utils import action_view_name, classproperty
from .list import ListBreadcrumbMixin


def _detail_view_label(instance, format_string):
    return _(force_str(format_string) % {"instance": force_str(instance)})


class DetailBreadcrumbMixin(ListBreadcrumbMixin):
    # Home / object List / str(object)
    detail_format_string = _("%(instance)s")

    @classproperty
    def detail_view_name(self):
        return action_view_name(
            model=self.model,
            action=self.detail_view_suffix,
            app_name=self.app_name,
            full=False,
        )

    @property
    def __detail_view_name(self):
        return action_view_name(
            model=self.model, action=self.detail_view_suffix, app_name=self.app_name
        )

    def detail_view_url(self, instance):
        if self.breadcrumb_use_pk:
            return reverse(
                self.__detail_view_name, kwargs={self.pk_url_kwarg: instance.pk}
            )

        return reverse(
            self.__detail_view_name,
            kwargs={self.slug_url_kwarg: getattr(instance, self.slug_field)},
        )

    @property
    def crumbs(self):
        return super(DetailBreadcrumbMixin, self).crumbs + [
            (
                partial(_detail_view_label, format_string=self.detail_format_string),
                self.detail_view_url,
            ),
        ]
