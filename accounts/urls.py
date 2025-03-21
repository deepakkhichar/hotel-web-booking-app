from django.urls import path

from accounts import views

urlpatterns = [
    path('register/customer/', views.customer_register, name='customer_register'),
    path('register/hotel/', views.hotel_register, name='hotel_register'),
    path('profile/', views.profile, name='profile'),
]
