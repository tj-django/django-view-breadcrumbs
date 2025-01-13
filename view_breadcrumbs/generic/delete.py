from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from ..utils import action_view_name, classproperty
from .detail import DetailBreadcrumbMixin


class DeleteBreadcrumbMixin(DetailBreadcrumbMixin):
    # Home / object List / object / Delete object
    delete_format_string = _("Delete %(instance)s")

    @classproperty
    def delete_view_name(self):
        return action_view_name(
            model=self.model,
            action=self.delete_view_suffix,
            app_name=self.app_name,
            full=False,
        )

    @property
    def __delete_view_name(self):
        return action_view_name(
            model=self.model, action=self.detail_view_suffix, app_name=self.app_name
        )

    def delete_view_url(self, instance):
        if self.breadcrumb_use_pk:
            return reverse(
                self.__delete_view_name, kwargs={self.pk_url_kwarg: instance.pk}
            )

        return reverse(
            self.__delete_view_name,
            kwargs={self.slug_url_kwarg: getattr(instance, self.slug_field)},
        )

    def delete_view_label(self, instance):
        if self.delete_format_string:
            return self.delete_format_string % {"instance": force_str(instance)}
        return _("Delete %(instance)s") % {"instance": force_str(instance)}

    @property
    def crumbs(self):
        return super(DeleteBreadcrumbMixin, self).crumbs + [
            (
                self.delete_view_label,
                self.delete_view_url,
            ),
        ]
