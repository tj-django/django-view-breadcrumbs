from django.utils.encoding import force_str

from .detail import DetailBreadcrumbMixin


class UpdateBreadcrumbMixin(DetailBreadcrumbMixin):

    @property
    def crumbs(self):
        return super(UpdateBreadcrumbMixin, self).crumbs + [
            (lambda o: f'Update: {force_str(o)}', '#'),
        ]
