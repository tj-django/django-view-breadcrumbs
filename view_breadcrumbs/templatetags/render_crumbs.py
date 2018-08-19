from django import template

register = template.Library()

@register.simple_tag
def render_crumbs(value):
    pass
