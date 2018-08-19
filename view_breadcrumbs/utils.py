from django.core.exceptions import AppRegistryNotReady


def get_app_name(model):
    if model._meta.installed:
        return getattr(model._meta, 'app_label')
    raise AppRegistryNotReady(
        '{model} is not installed or missing from the app registry.'.format(
            model=getattr(model._meta, 'app_label', model.__class__.__name__)
        )
    )

