from django.utils.encoding import force_str

from ..utils import action_view_name, classproperty
from .list import ListBreadcrumbMixin


class DetailBreadcrumbMixin(ListBreadcrumbMixin):
    # Home / object List / str(object)
    detail_format_string = "%s"

    @classproperty
    def detail_view_name(self):
        return action_view_name(
            model=self.model,
            action=self.detail_view_suffix,
            app_name=self.app_name,
            full=False,
        )

    @property
    def __detail_view_name(self):
        return action_view_name(
            model=self.model, action=self.detail_view_suffix, app_name=self.app_name
        )

    def detail_view_url(self, instance):
        return instance.get_absolute_url()

    def detail_view_label(self, instance):
        if self.detail_format_string:
            return self.detail_format_string % force_str(instance)
        return force_str(instance)

    @property
    def crumbs(self):
        return super(DetailBreadcrumbMixin, self).crumbs + [
            (
                self.detail_view_label,
                self.detail_view_url,
            ),
        ]
