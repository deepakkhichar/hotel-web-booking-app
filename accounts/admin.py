from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_hotel', 'is_customer', 'is_staff')
    list_filter = ('is_hotel', 'is_customer', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (('Custom Fields', {'fields': ('is_hotel', 'is_customer', 'phone', 'address')}),)


admin.site.register(User, CustomUserAdmin)
