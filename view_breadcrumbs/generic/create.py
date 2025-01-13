from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..utils import action_view_name, classproperty
from .list import ListBreadcrumbMixin


class CreateBreadcrumbMixin(ListBreadcrumbMixin):
    # Home / object List / Add object
    add_format_string = _("Add %(model)s")

    @classproperty
    def create_view_name(self):
        return action_view_name(
            model=self.model,
            action=self.create_view_suffix,
            app_name=self.app_name,
            full=False,
        )

    @property
    def __create_view_name(self):
        return action_view_name(
            model=self.model, action=self.create_view_suffix, app_name=self.app_name
        )

    @property
    def create_view_url(self):
        return reverse(self.__create_view_name)

    @property
    def create_view_label(self):
        if self.add_format_string:
            return self.add_format_string % {"model": self.model_name_title}
        return _("Add %(model)s") % {"model": self.model_name_title}

    @property
    def crumbs(self):
        return super(CreateBreadcrumbMixin, self).crumbs + [
            (
                self.create_view_label,
                self.create_view_url,
            ),
        ]
