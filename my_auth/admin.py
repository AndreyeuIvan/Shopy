from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from my_auth.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("phone_number",)}),
    )


admin.site.register(User, CustomUserAdmin)
