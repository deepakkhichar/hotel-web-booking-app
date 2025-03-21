from django.urls import path

from bookings import views

urlpatterns = [
    path('room/<int:room_id>/', views.book_room, name='book_room'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('', views.booking_list, name='booking_list'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
]
