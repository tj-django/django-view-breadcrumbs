from .base import BaseBreadcrumbMixin


class ListBreadcrumbMixin(BaseBreadcrumbMixin):
    # Home / object List
    @property
    def crumbs(self):
        return [(self.model_name_title_plural, self.list_view_name)]
