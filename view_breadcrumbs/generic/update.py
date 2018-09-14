from functools import partial

from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from .detail import DetailBreadcrumbMixin


def _update_view_label(instance, format_string):
    return _(force_str(format_string).format(force_str(instance)))


class UpdateBreadcrumbMixin(DetailBreadcrumbMixin):
    # Home / object List / object / Update object
    update_format_str = _('Update: {}')

    @property
    def crumbs(self):
        return super(UpdateBreadcrumbMixin, self).crumbs + [
            (partial(_update_view_label, format_string=self.update_format_str), '#'),
        ]
