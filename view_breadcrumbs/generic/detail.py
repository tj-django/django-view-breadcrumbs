from django.urls import reverse
from django.utils.encoding import force_str

from .base import BaseBreadcrumbMixin
from ..templatetags.app_url import action_view_name


class DetailBreadcrumbMixin(BaseBreadcrumbMixin):

    @property
    def crumbs(self):
        return [
            ('{}s'.format(self.model_name_title), self.list_view_name),
            (self._model_repr, self._detail_view_name),
        ]

    def _model_repr(self, instance):
        return force_str(instance)

    def _detail_view_name(self, instance):
        return reverse(action_view_name(instance, 'detail'), kwargs={'pk': instance.pk})
