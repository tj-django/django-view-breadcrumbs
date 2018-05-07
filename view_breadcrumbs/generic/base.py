import logging

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django_bootstrap_breadcrumbs.templatetags import (
    django_bootstrap_breadcrumbs
)

from ..templatetags.app_url import action_view_name
from ..utils import get_app_name

log = logging.getLogger(__name__)


def add_breadcrumb(context, label, view_name, **kwargs):
    return django_bootstrap_breadcrumbs.append_breadcrumb(
        context, label, view_name, (), kwargs,
    )


class BaseBreadcrumbMixin(object):
    add_home = True
    model = None
    app_name = get_app_name()

    @property
    def crumbs(self):
        raise NotImplementedError('{} should have a crumbs property.'.format(type(self).__name__))

    @property
    def model_name_title(self):
        return getattr(self.model._meta, 'verbose_name', '').title()

    @property
    def list_view_name(self):
        return reverse(action_view_name(self.model, 'list'))

    @property
    def edit_view_name(self):
        return lambda o: reverse(action_view_name(self.model, 'change'), kwargs={'pk': o.pk})

    def update_breadcrumbs(self, context):
        crumbs = self.crumbs
        if self.add_home:
            crumbs = [
                (
                    _(mark_safe('<span>Home</span>')), '/',
                ),
            ] + crumbs
        for crumb in crumbs:
            try:
                label, view_name = crumb
            except (TypeError, ValueError):
                raise ValueError(
                    'Breadrcumb requires a tuple of label and viewname.',
                )
            else:
                if hasattr(self, 'object') and self.object:
                    if callable(label):
                        label = label(self.object)
                    if callable(view_name):
                        view_name = view_name(self.object)
                add_breadcrumb(context, label, view_name)

    def get_context_data(self, **kwargs):
        ctx = {'request': self.request}
        if django_bootstrap_breadcrumbs.CONTEXT_KEY in self.request.META:
            django_bootstrap_breadcrumbs.clear_breadcrumbs(ctx)
        self.update_breadcrumbs(ctx)

        return super(BaseBreadcrumbMixin, self).get_context_data(**kwargs)
