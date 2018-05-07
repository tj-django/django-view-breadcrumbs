from django.utils.encoding import force_str

from .detail import DetailBreadcrumbMixin


def _update_view_label(instance):
    return 'Update: {}'.format(force_str(instance))


class UpdateBreadcrumbMixin(DetailBreadcrumbMixin):

    @property
    def crumbs(self):
        return super(UpdateBreadcrumbMixin, self).crumbs + [
            (_update_view_label, '#'),
        ]
