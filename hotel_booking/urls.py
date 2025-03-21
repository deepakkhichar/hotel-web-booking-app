from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from accounts.views import custom_logout
from hotel_booking.views import home, maps_proxy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('hotels/', include('hotels.urls')),
    path('bookings/', include('bookings.urls')),
    path('notifications/', include('notifications.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('api-docs/', TemplateView.as_view(template_name='api_docs.html'), name='api-docs'),
    path('maps-proxy/', maps_proxy, name='maps_proxy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
