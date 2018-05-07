from django.urls import reverse
from django.utils.encoding import force_str

from .base import BaseBreadcrumbMixin
from ..templatetags.app_url import action_view_name


class DetailBreadcrumbMixin(BaseBreadcrumbMixin):

    @property
    def crumbs(self):
        return [
            ('{}s'.format(self.model_name_title), self.list_view_name),
            (lambda o: force_str(o), lambda o: reverse(action_view_name(o, 'detail'), kwargs={'pk': o.pk})),
        ]
