from django.urls import reverse

from ..utils import action_view_name, classproperty


class DeleteBreadcrumbMixin(object):
    @classproperty
    def delete_view_name(self):
        return action_view_name(self.model, self.delete_view_suffix, full=False)

    @property
    def __delete_view_name(self):
        return action_view_name(self.model, self.detail_view_suffix)

    def delete_view_url(self, instance):
        return reverse(self.__delete_view_name, kwargs={"pk": instance.pk})
