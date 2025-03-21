from django.urls import path

from hotels import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('dashboard/', views.hotel_dashboard, name='hotel_dashboard'),
    path('edit/', views.edit_hotel, name='edit_hotel'),
    path('room/add/', views.add_room, name='add_room'),
    path('rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    path('rooms/<int:room_id>/data/', views.room_data, name='room_data'),
]
