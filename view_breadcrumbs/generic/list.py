from .base import BaseBreadcrumbMixin


class ListBreadcrumbMixin(BaseBreadcrumbMixin):

    @property
    def crumbs(self):
        return [
            ('{}s'.format(self.model_name_title), self.list_view_name),
        ]
