from django.utils.encoding import force_str

from .detail import DetailBreadcrumbMixin


class UpdateBreadcrumbMixin(DetailBreadcrumbMixin):

    @property
    def crumbs(self):
        return super(UpdateBreadcrumbMixin, self).crumbs + [
            (self._update_view_label, '#'),
        ]

    def _update_view_label(self, instance):
        return 'Update: {}'.format(force_str(instance))
