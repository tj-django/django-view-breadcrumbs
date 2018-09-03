from django.core.exceptions import AppRegistryNotReady


def get_app_name(model):
    if model._meta.installed:
        return getattr(model._meta, 'app_label')
    raise AppRegistryNotReady(
        '{model} is not installed or missing from the app registry.'.format(
            model=getattr(model._meta, 'app_label', model.__class__.__name__)
        )
    )

def action_view_name(model, action):
    return (
        '{0}:{1}_{2}'.format(
            get_app_name(model),
            getattr(model._meta, 'verbose_name', '').replace(' ', '_'),
            action,
        )
    )
