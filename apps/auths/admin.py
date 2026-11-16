from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.auths.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display: tuple[str, ...] = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter: tuple[str, ...] = ("is_staff", "is_active")
    search_fields: tuple[str, ...] = ("email", "first_name", "last_name")
    ordering: tuple[str, ...] = ("email",)

    fieldsets: tuple = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets: tuple = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password"),
            },
        ),
    )
