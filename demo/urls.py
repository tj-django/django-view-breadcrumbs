"""
Examples:
    For the test LIST and CRUD views.
    [
        path('test/', views.TestListsView.as_view(), name='test_list'),
        path('test/add/', views.TestCreateView.as_view(), name='test_add'),
        path('test/<int:pk>/change', views.TestUpdateView.as_view(), name='test_change'),
        ...
    ]
"""
try:
    from django.urls import include
    from django.urls import re_path as path
except ImportError:
    from django.conf.urls import url as path, include

from .views import (
    TestCreateView,
    TestDeleteView,
    TestDetailView,
    TestHomeView,
    TestListsView,
    TestModelMultiTableView,
    TestModelSingleTableView,
    TestUpdateView,
    TestView, LibraryListsView, LibraryDetailView, LibraryCreateView, LibraryUpdateView, LibraryDeleteView,
)

app_name = "demo"


test_patterns = (
    [
        # Home view
        path("^$", TestHomeView.as_view(), name="test_root"),
        # Custom view
        path("^test/custom/$", TestView.as_view(), name="test_view"),
        # CRUD views.
        path("^tests/$", TestListsView.as_view(), name=TestListsView.list_view_name),
        path(
            "^tests/add/$",
            TestCreateView.as_view(),
            name=TestCreateView.create_view_name,
        ),
        path(
            "^tests/(?P<pk>[0-9]+)/$",
            TestDetailView.as_view(),
            name=TestDetailView.detail_view_name,
        ),
        path(
            "^tests/(?P<pk>[0-9]+)/update/$",
            TestUpdateView.as_view(),
            name=TestUpdateView.update_view_name,
        ),
        path(
            "^tests/(?P<pk>[0-9]+)/delete/$",
            TestDeleteView.as_view(),
            name=TestDeleteView.delete_view_name,
        ),
        path("^libraryies/$", LibraryListsView.as_view(), name=LibraryListsView.list_view_name),
        path(
            "^libraryies/(?P<pk>[0-9]+)/$",
            LibraryDetailView.as_view(),
            name=LibraryDetailView.detail_view_name,
        ),
        path(
            "^libraries/add/$",
            LibraryCreateView.as_view(),
            name=LibraryCreateView.create_view_name,
        ),
        path(
            "^libraries/(?P<pk>[0-9]+)/update/$",
            LibraryUpdateView.as_view(),
            name=LibraryUpdateView.update_view_name,
        ),
        path(
            "^libraries/(?P<pk>[0-9]+)/delete/$",
            LibraryDeleteView.as_view(),
            name=LibraryDeleteView.delete_view_name,
        ),
        path(
            "^tests/lists/$",
            TestModelSingleTableView.as_view(),
            name="test_model_table",
        ),
        path(
            "^tests/lists/multiple/$",
            TestModelMultiTableView.as_view(),
            name="test_model_multi_table",
        ),
    ],
    app_name,
)


urlpatterns = [path("", include(test_patterns, namespace=app_name))]
