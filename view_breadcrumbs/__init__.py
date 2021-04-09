"""Top-level package for view_breadcrumbs."""

__author__ = """Tonye Jack"""
__email__ = "jtonye@ymail.com"
__version__ = "2.0.0"

from .generic import (
    BaseBreadcrumbMixin,
    CreateBreadcrumbMixin,
    DetailBreadcrumbMixin,
    ListBreadcrumbMixin,
    UpdateBreadcrumbMixin,
    DeleteBreadcrumbMixin,
)

__all__ = [
    "BaseBreadcrumbMixin",
    "CreateBreadcrumbMixin",
    "DetailBreadcrumbMixin",
    "ListBreadcrumbMixin",
    "UpdateBreadcrumbMixin",
    "DeleteBreadcrumbMixin",
]
