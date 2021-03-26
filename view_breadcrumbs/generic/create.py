from django.utils.translation import gettext_lazy as _

from .list import ListBreadcrumbMixin


class CreateBreadcrumbMixin(ListBreadcrumbMixin):
    # Home / object List / Add object
    add_format_string = _("Add %(model)s")

    @property
    def crumbs(self):
        return super(CreateBreadcrumbMixin, self).crumbs + [
            (_(self.add_format_string % {"model": self.model_name_title}), "#"),
        ]
