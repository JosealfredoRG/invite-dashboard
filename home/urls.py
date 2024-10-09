from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('invitacion', views.invite_view, name='invite'),
    path('invitacion/<int:event_id>/<int:guest_id>/', views.guest_invite_view, name='guest_invite_view'),
    path('eventos', views.event_list, name='event_list'),
    path('create_event', views.create_event, name='create_event'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event_delete', views.event_delete, name='event_delete'),
    path('create_guest/<int:event_id>/', views.create_guest, name='create_guest'),
    path('edit_guest/<int:event_id>/<int:guest_id>/', views.edit_guest, name='edit_guest'),
    path('upload_guests/<int:event_id>', views.upload_guests, name='upload_guests'),
    path('delete_guest/<int:event_id>/', views.delete_guest, name='delete_guest'),
    path('delete_all_guest/<int:event_id>/', views.delete_all_guest, name='delete_all_guest'),
    path('invite_guest/<int:guest_id>/', views.invite_guest, name='invite_guest'),
]
