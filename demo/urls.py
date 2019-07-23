"""
Examples:
    For the test LIST and CRUD views.
    [
        path('test/', views.TestListsView.as_view(), name='test_list'),
        path('test/add/', views.TestCreateView.as_view(), name='test_add'),
        path('test/<int:pk>/change', views.TestUpdateView.as_view(), name='test_change'),
        path('test/<int:pk>/delete', views.TestDeleteView.as_view(), name='test_delete'),
        path('test/<int:pk>/delete_error', views.TestDeleteErrorView.as_view(), name='test_delete_error'),
    ]
"""
try:
   from django.urls import re_path as path, include
except ImportError:
   from django.conf.urls import url as path, include

from . import views

app_name = 'demo'



test_patterns = ([
   # Home view
   path('^$', views.TestHomeView.as_view(), name='test_root'),
   # Custom view
   path('^test/custom/$', views.TestView.as_view(), name='test_view'),
   # CRUD views.
   path('^tests/$', views.TestListsView.as_view(), name='testmodel_list'),
   path('^tests/(?P<pk>\d+)/$', views.TestDetailView.as_view(), name='testmodel_detail'),
], app_name)


urlpatterns = [
   path('', include(test_patterns, namespace=app_name))
]

