from django.urls import reverse

from ..utils import action_view_name, classproperty
from .base import BaseModelBreadcrumbMixin


class ListBreadcrumbMixin(BaseModelBreadcrumbMixin):
    # Home / object List

    @classproperty
    def list_view_name(self):
        return action_view_name(
            model=self.model,
            action=self.list_view_suffix,
            app_name=self.app_name,
            full=False,
        )

    @property
    def __list_view_name(self):
        return action_view_name(
            model=self.model, action=self.list_view_suffix, app_name=self.app_name
        )

    @property
    def list_view_url(self):
        return reverse(self.__list_view_name)

    @property
    def crumbs(self):
        return [(self.model_name_title_plural, self.list_view_url)]
