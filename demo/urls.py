"""
Examples:
    For the events LIST and CRUD views.
    [
        path('events/', views.EventLists.as_view(), name='event_list'),
        path('event/add/', views.EventCreate.as_view(), name='event_add'),
        path('event/<int:pk>/change', views.EventUpdate.as_view(), name='event_change'),
        path('event/<int:pk>/delete', views.EventDelete.as_view(), name='event_delete'),
        path('event/<int:pk>/delete_error', views.EventDeleteError.as_view(), name='event_delete_error'),
    ]
"""

from django.urls import path

from . import views

app_name = 'demo'

urlpatterns = [
   path('', views.TestView.as_view(), name='test_view'),
]
