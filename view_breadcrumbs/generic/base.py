import logging

from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from ..templatetags.view_breadcrumbs import append_breadcrumb, CONTEXT_KEY, clear_breadcrumbs
from ..utils import (
    get_app_name, action_view_name, verbose_name_raw, verbose_name_plural_raw,
)

log = logging.getLogger(__name__)


def add_breadcrumb(context, label, view_name, **kwargs):
    return append_breadcrumb(context, label, view_name, (), kwargs)


class BaseBreadcrumbMixin(object):
    add_home = True
    model = None

    list_view_suffix = 'list'
    change_view_suffix = 'change'
    detail_view_suffix = 'detail'

    home_path = '/'

    @cached_property
    def home_label(self):
        return _(getattr(settings, 'BREADCRUMBS_HOME_LABEL', 'Home'))

    @cached_property
    def app_name(self):
        return get_app_name(self.model)

    @property
    def crumbs(self):
        raise NotImplementedError('{} should have a crumbs property.'.format(type(self).__name__))

    @property
    def model_name_title_plural(self):
        return verbose_name_plural_raw(self.model).title()

    @property
    def model_name_title(self):
        return verbose_name_raw(self.model).title()

    @property
    def list_view_name(self):
        return reverse(action_view_name(self.model, self.list_view_suffix))

    def edit_view_name(self, instance):
        return reverse(action_view_name(self.model, self.change_view_suffix), kwargs={'pk': instance.pk})

    def update_breadcrumbs(self, context):
        crumbs = self.crumbs
        if self.add_home:
            crumbs = [(self.home_label, self.home_path)] + crumbs
        for crumb in crumbs:
            try:
                label, view_name = crumb
            except (TypeError, ValueError):
                raise ValueError('Breadcrumb requires a tuple of label and view name.')
            else:
                if hasattr(self, 'object') and self.object:
                    if callable(label):
                        label = label(self.object)
                    if callable(view_name):
                        view_name = view_name(self.object)
                add_breadcrumb(context, label, view_name)

    def get_context_data(self, **kwargs):
        ctx = {'request': self.request}
        if CONTEXT_KEY in self.request.META:
            clear_breadcrumbs(ctx)
        self.update_breadcrumbs(ctx)

        return super(BaseBreadcrumbMixin, self).get_context_data(**kwargs)
