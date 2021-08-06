import logging

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from view_breadcrumbs.constants import (
    CREATE_VIEW_SUFFIX,
    DELETE_VIEW_SUFFIX,
    DETAIL_VIEW_SUFFIX,
    LIST_VIEW_SUFFIX,
    UPDATE_VIEW_SUFFIX,
)

from ..templatetags.view_breadcrumbs import (
    CONTEXT_KEY,
    append_breadcrumb,
    clear_breadcrumbs,
)
from ..utils import get_verbose_name, get_verbose_name_plural

log = logging.getLogger(__name__)


def add_breadcrumb(context, label, view_name, **kwargs):
    return append_breadcrumb(context, label, view_name, (), kwargs)


class BaseBreadcrumbMixin(object):
    add_home = True
    model = None
    home_path = "/"
    home_label = None

    @property
    def crumbs(self):
        raise NotImplementedError(
            _(
                "%(class_name)s should have a crumbs property."
                % {"class_name": type(self).__name__}
            )
        )

    def update_breadcrumbs(self, context):
        crumbs = self.crumbs
        if self.add_home:
            home_label = self.home_label or _(
                getattr(settings, "BREADCRUMBS_HOME_LABEL", _("Home"))
            )
            crumbs = [(home_label, self.home_path)] + crumbs
        for crumb in crumbs:
            try:
                label, view_name = crumb
            except (TypeError, ValueError):
                raise ValueError(
                    _("Breadcrumb requires a tuple of label and view name.")
                )
            else:
                if hasattr(self, "object") and self.object:
                    if callable(label):
                        label = label(self.object)
                    if callable(view_name):
                        view_name = view_name(self.object)
                add_breadcrumb(context, label, view_name)

    def get_context_data(self, **kwargs):
        ctx = {"request": self.request}
        if CONTEXT_KEY in self.request.META:
            clear_breadcrumbs(ctx)
        self.update_breadcrumbs(ctx)

        return super(BaseBreadcrumbMixin, self).get_context_data(**kwargs)


class BaseModelBreadcrumbMixin(BaseBreadcrumbMixin):
    breadcrumb_use_pk = True
    app_name = None

    list_view_suffix = LIST_VIEW_SUFFIX
    create_view_suffix = CREATE_VIEW_SUFFIX
    update_view_suffix = UPDATE_VIEW_SUFFIX
    delete_view_suffix = DELETE_VIEW_SUFFIX
    detail_view_suffix = DETAIL_VIEW_SUFFIX

    @property
    def model_name_title(self):
        return get_verbose_name(self.model).title()

    @property
    def model_name_title_plural(self):
        return get_verbose_name_plural(self.model).title()
