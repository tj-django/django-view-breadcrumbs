from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from .list import ListBreadcrumbMixin


class CreateBreadcrumbMixin(ListBreadcrumbMixin):
    # Home / object List / Add object
    add_format_string = _('Add {}')

    @property
    def crumbs(self):
        return super(CreateBreadcrumbMixin, self).crumbs + [
            (_(force_str(self.add_format_string).format(self.model_name_title)), '#'),
        ]
