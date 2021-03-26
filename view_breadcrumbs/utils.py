from django.core.exceptions import AppRegistryNotReady
from django.utils.encoding import force_str
from django.utils.translation import override
from django.utils.translation import ugettext_lazy as _


def get_verbose_name(model):
    return force_str(model._meta.verbose_name)


def get_verbose_name_plural(model):
    return force_str(model._meta.verbose_name_plural)


def get_app_label(model):
    return force_str(model._meta.app_label)


def get_model_name(model):
    return force_str(model._meta.model_name)


def get_app_name(model):
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


def action_view_name(model, action):
    app_label, model_name = get_app_name(model)

    with override(None):
        return "%(app_label)s:%(model_name)s_%(action)s" % {
            "app_label": app_label,
            "model_name": model_name.lower().replace(" ", "_"),
            "action": action,
        }
