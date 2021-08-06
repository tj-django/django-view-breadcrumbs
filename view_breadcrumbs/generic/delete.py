from django.urls import reverse

from ..utils import action_view_name, classproperty
from .list import ListBreadcrumbMixin


class DeleteBreadcrumbMixin(ListBreadcrumbMixin):
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
