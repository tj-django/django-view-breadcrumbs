from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .list import ListBreadcrumbMixin
from ..utils import action_view_name, classproperty


class CreateBreadcrumbMixin(ListBreadcrumbMixin):
    # Home / object List / Add object
    add_format_string = _("Add %(model)s")

    @classproperty
    def create_view_name(self):
        return action_view_name(self.model, self.create_view_suffix, full=False)

    @property
    def __create_view_name(self):
        return action_view_name(self.model, self.create_view_suffix)

    @property
    def create_view_url(self):
        return reverse(self.__create_view_name)

    @property
    def crumbs(self):
        return super(CreateBreadcrumbMixin, self).crumbs + [
            (
                _(self.add_format_string % {"model": self.model_name_title}),
                self.create_view_url,
            ),
        ]
