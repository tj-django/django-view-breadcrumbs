from django.urls import reverse

from .base import BaseModelBreadcrumbMixin
from ..utils import action_view_name, classproperty


class ListBreadcrumbMixin(BaseModelBreadcrumbMixin):
    # Home / object List

    @classproperty
    def list_view_name(self):
        return action_view_name(self.model, self.list_view_suffix, full=False)

    @property
    def __list_view_name(self):
        return action_view_name(self.model, self.list_view_suffix)

    @property
    def list_view_url(self):
        return reverse(self.__list_view_name)

    @property
    def crumbs(self):
        return [(self.model_name_title_plural, self.list_view_url)]
