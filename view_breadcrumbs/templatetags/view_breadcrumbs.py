# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

import logging
from functools import wraps
from inspect import ismethod

from django import VERSION, template
from django.conf import settings
from django.db.models import Model
from django.template.loader import render_to_string
from django.utils.encoding import smart_str

from view_breadcrumbs.constants import (
    CREATE_VIEW_SUFFIX,
    DELETE_VIEW_SUFFIX,
    DETAIL_VIEW_SUFFIX,
    LIST_VIEW_SUFFIX,
    UPDATE_VIEW_SUFFIX,
)
from view_breadcrumbs.utils import action_view_name

if VERSION >= (2, 0):
    from django.urls import NoReverseMatch, Resolver404, resolve, reverse
else:
    from django.core.urlresolvers import NoReverseMatch, Resolver404, resolve, reverse

logger = logging.getLogger(__name__)

register = template.Library()


CONTEXT_KEY = "DJANGO_VIEW_BREADCRUMB_LINKS"


def log_request_not_found():
    if VERSION < (1, 8):  # pragma: nocover
        logger.error(
            "request object not found in context! Check if "
            "'django.core.context_processors.request' is in "
            "TEMPLATE_CONTEXT_PROCESSORS"
        )
    else:  # pragma: nocover
        logger.error(
            "request object not found in context! Check if "
            "'django.template.context_processors.request' is in the "
            "'context_processors' option of your template settings."
        )


def requires_request(func):
    @wraps(func)
    def wrapped(context, *args, **kwargs):
        if "request" in context:
            return func(context, *args, **kwargs)

        log_request_not_found()
        return ""

    return wrapped


@requires_request
def append_breadcrumb(context, label, viewname, args, kwargs):
    context["request"].META[CONTEXT_KEY] = context["request"].META.get(
        CONTEXT_KEY, []
    ) + [(label, viewname, args, kwargs)]


@register.simple_tag(takes_context=True)
@requires_request
def render_breadcrumbs(context, *args):
    """
    Render breadcrumbs html using bootstrap css classes.
    """

    try:
        template_path = args[0]
    except IndexError:
        template_path = getattr(
            settings, "BREADCRUMBS_TEMPLATE", "view_breadcrumbs/bootstrap5.html"
        )

    links = []
    for (label, viewname, view_args, view_kwargs) in context["request"].META.get(
        CONTEXT_KEY, []
    ):
        if (
            isinstance(viewname, Model)
            and hasattr(viewname, "get_absolute_url")
            and ismethod(viewname.get_absolute_url)
        ):
            url = viewname.get_absolute_url(*view_args, **view_kwargs)
        else:
            try:
                try:
                    # 'resolver_match' introduced in Django 1.5
                    current_app = context["request"].resolver_match.namespace
                except AttributeError:
                    try:
                        resolver_match = resolve(context["request"].path)
                        current_app = resolver_match.namespace
                    except Resolver404:
                        current_app = None
                url = reverse(
                    viewname=viewname,
                    args=view_args,
                    kwargs=view_kwargs,
                    current_app=current_app,
                )
            except NoReverseMatch:
                url = viewname
        links.append((url, smart_str(label) if label else label))

    if not links:
        return ""

    if VERSION > (1, 8):  # pragma: nocover
        # RequestContext is deprecated in recent django
        # https://docs.djangoproject.com/en/1.10/ref/templates/upgrading/
        context = context.flatten()

    context["breadcrumbs"] = links
    context["breadcrumbs_total"] = len(links)

    return render_to_string(template_path, context)


@register.simple_tag(takes_context=True)
@requires_request
def clear_breadcrumbs(context, *args):
    """
    Removes all currently added breadcrumbs.
    """

    context["request"].META.pop(CONTEXT_KEY, None)
    return ""


def _get_model(model):
    if model is None:
        raise ValueError("Invalid model")

    if isinstance(model, str):
        from django.apps import apps

        model = apps.get_model(model)

    return model


def _view_url(model, suffix, app_name=None):
    view_name = action_view_name(
        model=_get_model(model), app_name=app_name, action=suffix
    )
    return reverse(view_name)


@register.simple_tag()
def list_view_url(model, app_name=None, suffix=LIST_VIEW_SUFFIX):
    return _view_url(model=model, app_name=app_name, suffix=suffix)


@register.simple_tag()
def create_view_url(model, app_name=None, suffix=CREATE_VIEW_SUFFIX):
    return _view_url(model=model, app_name=app_name, suffix=suffix)


def _object_url(
    instance,
    suffix,
    use_pk=True,
    pk_url_kwarg="pk",
    slug_url_kwarg="slug",
    app_name=None,
    slug_field="slug",
):
    model = instance.__class__
    view_name = action_view_name(model=model, action=suffix, app_name=app_name)

    if use_pk:
        return reverse(view_name, kwargs={pk_url_kwarg: instance.pk})

    return reverse(
        view_name,
        kwargs={slug_url_kwarg: getattr(instance, slug_field)},
    )


@register.simple_tag(takes_context=True)
def update_view_url(
    context,
    use_pk=True,
    pk_url_kwarg="pk",
    slug_url_kwarg="slug",
    slug_field="slug",
    app_name=None,
    suffix=UPDATE_VIEW_SUFFIX,
):
    return _object_url(
        instance=context["object"],
        use_pk=use_pk,
        pk_url_kwarg=pk_url_kwarg,
        slug_url_kwarg=slug_url_kwarg,
        slug_field=slug_field,
        app_name=app_name or getattr(context["view"], "app_name", None),
        suffix=suffix,
    )


@register.simple_tag()
def update_instance_view_url(
    instance,
    use_pk=True,
    pk_url_kwarg="pk",
    slug_url_kwarg="slug",
    slug_field="slug",
    app_name=None,
    suffix=UPDATE_VIEW_SUFFIX,
):
    return _object_url(
        instance=instance,
        use_pk=use_pk,
        pk_url_kwarg=pk_url_kwarg,
        slug_url_kwarg=slug_url_kwarg,
        slug_field=slug_field,
        app_name=app_name,
        suffix=suffix,
    )


@register.simple_tag(takes_context=True)
def delete_view_url(
    context,
    use_pk=True,
    pk_url_kwarg="pk",
    slug_url_kwarg="slug",
    slug_field="slug",
    suffix=DELETE_VIEW_SUFFIX,
    app_name=None,
):
    return _object_url(
        instance=context["object"],
        use_pk=use_pk,
        pk_url_kwarg=pk_url_kwarg,
        slug_url_kwarg=slug_url_kwarg,
        slug_field=slug_field,
        app_name=app_name or getattr(context["view"], "app_name", None),
        suffix=suffix,
    )


@register.simple_tag()
def delete_instance_view_url(
    instance,
    use_pk=True,
    pk_url_kwarg="pk",
    slug_url_kwarg="slug",
    slug_field="slug",
    suffix=DELETE_VIEW_SUFFIX,
    app_name=None,
):
    return _object_url(
        instance=instance,
        use_pk=use_pk,
        pk_url_kwarg=pk_url_kwarg,
        slug_url_kwarg=slug_url_kwarg,
        slug_field=slug_field,
        app_name=app_name,
        suffix=suffix,
    )


@register.simple_tag(takes_context=True)
def detail_view_url(
    context,
    use_pk=True,
    pk_url_kwarg="pk",
    slug_url_kwarg="slug",
    slug_field="slug",
    suffix=DETAIL_VIEW_SUFFIX,
    app_name=None,
):
    return _object_url(
        instance=context["object"],
        use_pk=use_pk,
        pk_url_kwarg=pk_url_kwarg,
        slug_url_kwarg=slug_url_kwarg,
        slug_field=slug_field,
        suffix=suffix,
        app_name=app_name or getattr(context["view"], "app_name", None),
    )


@register.simple_tag()
def detail_instance_view_url(
    instance,
    use_pk=True,
    pk_url_kwarg="pk",
    slug_url_kwarg="slug",
    slug_field="slug",
    suffix=DETAIL_VIEW_SUFFIX,
    app_name=None,
):
    return _object_url(
        instance=instance,
        use_pk=use_pk,
        pk_url_kwarg=pk_url_kwarg,
        slug_url_kwarg=slug_url_kwarg,
        slug_field=slug_field,
        suffix=suffix,
        app_name=app_name,
    )
