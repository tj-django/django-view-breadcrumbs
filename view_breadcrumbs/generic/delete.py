from django.urls import reverse

from .list import ListBreadcrumbMixin
from ..utils import action_view_name, classproperty


class DeleteBreadcrumbMixin(ListBreadcrumbMixin):
    @classproperty
    def delete_view_name(self):
        return action_view_name(self.model, self.delete_view_suffix, full=False)

    @property
    def __delete_view_name(self):
        return action_view_name(self.model, self.detail_view_suffix)

    def delete_view_url(self, instance):
        if self.breadcrumb_use_pk:
            return reverse(
                self.__delete_view_name, kwargs={self.pk_url_kwarg: instance.pk}
            )

        return reverse(
            self.__delete_view_name,
            kwargs={self.slug_url_kwarg: getattr(instance, self.slug_field)},
        )
