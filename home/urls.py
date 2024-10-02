from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('invitacion', views.invite_view, name='invite'),
    path('eventos', views.event_list, name='event_list'),
    path('create_event', views.create_event, name='create_event'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event_delete', views.event_delete, name='event_delete'),
    path('create_guest/<int:event_id>/', views.create_guest, name='create_guest'),

]
