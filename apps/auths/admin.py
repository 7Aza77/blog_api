from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import BooleanRadioFilter
from unfold.decorators import display

from apps.auths.forms import (
    CustomAdminPasswordChangeForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from apps.auths.models import User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    """Group model admin configured for Unfold."""

    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    """Custom user model admin configured for Unfold."""

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = CustomAdminPasswordChangeForm

    list_display = (
        'show_header',
        'show_is_active',
        'show_is_staff',
        'show_posts_count',
    )
    list_filter = (
        ('is_active', BooleanRadioFilter),
        ('is_staff', BooleanRadioFilter),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (
            'Personal info',
            {
                'classes': ('tab',),
                'fields': ('email', 'first_name', 'last_name'),
            },
        ),
        (
            'Permissions',
            {
                'classes': ('tab',),
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Important dates',
            {
                'classes': ('tab',),
                'fields': ('last_login',),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
            },
        ),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[User]:
        """Annotate queryset with related posts count."""
        return super().get_queryset(request).annotate(posts_count=Count('posts'))

    @display(description='User', header=True)
    def show_header(self, obj: User) -> tuple[str, str, str]:
        """Display composite header with full name, email, and initials circle."""
        full_name = obj.get_full_name() or obj.email
        initials = f'{obj.first_name[:1]}{obj.last_name[:1]}'.upper() or 'U'
        return full_name, obj.email, initials

    @display(
        description='Active',
        label={
            True: 'success',
            False: 'danger',
        },
    )
    def show_is_active(self, obj: User) -> bool:
        """Display colored active status label."""
        return obj.is_active

    @display(
        description='Staff',
        label={
            True: 'info',
            False: 'warning',
        },
    )
    def show_is_staff(self, obj: User) -> bool:
        """Display colored staff status label."""
        return obj.is_staff

    @display(description='Posts', ordering='posts_count')
    def show_posts_count(self, obj: User) -> int:
        """Display annotated posts count with column sorting."""
        return getattr(obj, 'posts_count', 0)

    # TODO(hw2): bulk action to activate selected users
    # TODO(hw2): bulk action to deactivate selected users


