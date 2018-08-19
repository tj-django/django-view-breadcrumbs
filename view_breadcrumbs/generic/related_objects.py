from django.urls import reverse
from django.utils.encoding import force_str

from .base import BaseBreadcrumbMixin
from ..utils import action_view_name


class RelatedObjectBreadcrumb(BaseBreadcrumbMixin):
    """
    Breadcrumb for related objects.

    Notes:
        The self.object must be an instance of the parent object.
    """
    parent_breadcrumb_views = ()
    _crud_view_names = {'change', 'detail'}
    _list_view_names = {'list'}

    @property
    def crumbs(self):
        crumbs = []
        for view in self.parent_breadcrumb_views:
            view_name = action_view_name(self.object, view)
            if view in self._list_view_names:
                crumbs.append((f'{self.object.model._meta.object_name}s', reverse(view_name),))
            elif view in self._crud_view_names:
                crumbs.append(
                    (f'{force_str(self.object)}', reverse(view_name, kwargs={'pk':self.object.pk}),),
                )

        return crumbs + [((self.model._meta.verbose_name_plural).title(), '#')]
