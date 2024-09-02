from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('invitacion', views.invite_view, name='invite'),
]
