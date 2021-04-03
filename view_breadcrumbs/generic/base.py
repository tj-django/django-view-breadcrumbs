import logging

from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..templatetags.view_breadcrumbs import (
    CONTEXT_KEY,
    append_breadcrumb,
    clear_breadcrumbs,
)
from ..utils import get_verbose_name_plural, get_verbose_name, action_view_name, classproperty

log = logging.getLogger(__name__)


def add_breadcrumb(context, label, view_name, **kwargs):
    return append_breadcrumb(context, label, view_name, (), kwargs)


class BaseBreadcrumbMixin(object):
    add_home = True
    model = None
    home_path = "/"

    @cached_property
    def home_label(self):
        return _(getattr(settings, "BREADCRUMBS_HOME_LABEL", _("Home")))

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
            crumbs = [(self.home_label, self.home_path)] + crumbs
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
    list_view_suffix = _("list")
    create_view_suffix = _("create")
    update_view_suffix = _("update")
    delete_view_suffix = _("delete")
    detail_view_suffix = _("detail")

    @property
    def model_name_title(self):
        return get_verbose_name(self.model).title()

    @property
    def model_name_title_plural(self):
        return get_verbose_name_plural(self.model).title()

    @classproperty
    def delete_view_name(self):
        return action_view_name(self.model, self.delete_view_suffix, full=False)

    @property
    def __delete_view_name(self):
        return action_view_name(self.model, self.detail_view_suffix)

    def delete_view_url(self, instance):
        return reverse(self.__delete_view_name, kwargs={"pk": instance.pk})
