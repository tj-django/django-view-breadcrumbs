# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

import logging
from inspect import ismethod

from django import template, VERSION
from django.conf import settings
from django.db.models import Model
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.safestring import SafeString
from six import wraps

if VERSION >= (2, 0):
    from django.urls import (
        reverse, resolve, NoReverseMatch, Resolver404
    )
else:
    from django.core.urlresolvers import (
        reverse, resolve, NoReverseMatch, Resolver404
    )

logger = logging.getLogger(__name__)

register = template.Library()


CONTEXT_KEY = 'DJANGO_VIEW_BREADCRUMB_LINKS'


def log_request_not_found():
    if VERSION < (1, 8):  # pragma: nocover
        logger.error("request object not found in context! Check if "
                     "'django.core.context_processors.request' is in "
                     "TEMPLATE_CONTEXT_PROCESSORS")
    else:  # pragma: nocover
        logger.error("request object not found in context! Check if "
                     "'django.template.context_processors.request' is in the "
                     "'context_processors' option of your template settings.")


def requires_request(func):
    @wraps(func)
    def wrapped(context, *args, **kwargs):
        if 'request' in context:
            return func(context, *args, **kwargs)

        log_request_not_found()
        return ''

    return wrapped


@requires_request
def append_breadcrumb(context, label, viewname, args, kwargs):
    context['request'].META[CONTEXT_KEY] = (
        context['request'].META.get(CONTEXT_KEY, []) + [(label, viewname, args, kwargs)]
    )


@register.simple_tag(takes_context=True)
@requires_request
def render_breadcrumbs(context, *args):
    """
    Render breadcrumbs html using bootstrap css classes.
    """

    try:
        template_path = args[0]
    except IndexError:
        template_path = getattr(settings, 'BREADCRUMBS_TEMPLATE',
                                'view_breadcrumbs/bootstrap4.html')

    links = []
    for (label, viewname, view_args, view_kwargs) in context['request'].META.get(CONTEXT_KEY, []):
        if isinstance(viewname, Model) and hasattr(viewname, 'get_absolute_url') and ismethod(viewname.get_absolute_url):
            url = viewname.get_absolute_url(*view_args, **view_kwargs)
        else:
            try:
                try:
                    # 'resolver_match' introduced in Django 1.5
                    current_app = context['request'].resolver_match.namespace
                except AttributeError:
                    try:
                        resolver_match = resolve(context['request'].path)
                        current_app = resolver_match.namespace
                    except Resolver404:
                        current_app = None
                url = reverse(viewname=viewname, args=view_args,
                              kwargs=view_kwargs, current_app=current_app)
            except NoReverseMatch:
                url = viewname
        links.append((url, smart_text(label) if label else label))

    if not links:
        return ''

    if VERSION > (1, 8):  # pragma: nocover
        # RequestContext is deprecated in recent django
        # https://docs.djangoproject.com/en/1.10/ref/templates/upgrading/
        context = context.flatten()

    context['breadcrumbs'] = links
    context['breadcrumbs_total'] = len(links)

    return SafeString(render_to_string(template_path, context))


@register.simple_tag(takes_context=True)
@requires_request
def clear_breadcrumbs(context, *args):
    """
    Removes all currently added breadcrumbs.
    """

    context['request'].META.pop(CONTEXT_KEY, None)
    return ''
