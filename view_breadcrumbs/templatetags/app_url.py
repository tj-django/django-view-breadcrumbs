from django import template
from django.urls import reverse

from ..utils import get_app_name

register = template.Library()


@register.filter
def action_view_name(value, action):
    return (
        f'{get_app_name()}:{getattr(value._meta, "verbose_name", "").replace(" ", "_")}_{action}'
    )


@register.filter(is_safe=False)
def action_object_url(value, action):
    return reverse(action_view_name(value, action), kwargs={'pk': value.pk})
