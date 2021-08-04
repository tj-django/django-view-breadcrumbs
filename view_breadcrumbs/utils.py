from django.core.exceptions import AppRegistryNotReady
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.utils.translation import override


class classproperty:
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


def get_verbose_name(model):
    return force_str(model._meta.verbose_name)


def get_verbose_name_plural(model):
    return force_str(model._meta.verbose_name_plural)


def get_app_label(model):
    return force_str(model._meta.app_label)


def get_model_name(model):
    return force_str(model._meta.model_name)


def get_model_info(model):
    if model._meta.installed:
        return get_app_label(model), get_model_name(model)

    raise AppRegistryNotReady(
        _("%(model)s is not installed or missing from the app registry.")
        % {
            "model": (
                getattr(
                    model._meta,
                    "app_label",
                    model.__class__.__name__,
                )
            )
        }
    )


def action_view_name(*, model, action, app_name=None, full=True):
    if app_name is None:
        app_name, model_name = get_model_info(model)
    else:
        model_name = get_model_name(model)

    with override(None):
        if full:
            return "%(app_name)s:%(model_name)s_%(action)s" % {
                "app_name": app_name,
                "model_name": model_name.lower().replace(" ", "_"),
                "action": action,
            }

        return "%(model_name)s_%(action)s" % {
            "model_name": model_name.lower().replace(" ", "_"),
            "action": action,
        }
