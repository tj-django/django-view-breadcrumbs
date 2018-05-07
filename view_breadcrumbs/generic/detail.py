from django.urls import reverse
from django.utils.encoding import force_str

from .base import BaseBreadcrumbMixin
from ..templatetags.app_url import action_view_name


def _model_repr(instance):
    return force_str(instance)


def _detail_view_name(instance):
    return reverse(action_view_name(instance, 'detail'), kwargs={'pk': instance.pk})


class DetailBreadcrumbMixin(BaseBreadcrumbMixin):

    @property
    def crumbs(self):
        return [
            ('{}s'.format(self.model_name_title), self.list_view_name),
            (_model_repr, _detail_view_name),
        ]
