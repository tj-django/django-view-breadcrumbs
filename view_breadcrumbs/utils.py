from django.core.exceptions import AppRegistryNotReady
from django.utils.encoding import force_text
from django.utils.translation import override


def get_app_name(model):
    if model._meta.installed:
        return getattr(model._meta, 'label', '.').split('.')

    raise AppRegistryNotReady(
        '{model} is not installed or missing from the app registry.'.format(
            model=getattr(model._meta, 'app_label', model.__class__.__name__)
        )
    )

def action_view_name(model, action):
    app_label, model_name = get_app_name(model)

    if app_label and model_name:
        return (
            '{0}:{1}_{2}'.format(
                app_label,
                model_name.lower().replace(' ', '_'),
                action,
            )
        )


def verbose_name_raw(model):
    return force_text(model._meta.verbose_name_raw)


def verbose_name_plural_raw(model):
    with override(None):
        return force_text(model._meta.verbose_name_plural)
