from django.urls import path

from . import views


urlpatterns = [
   path('list/', views.TestView.as_view(), name='test_view'),
]