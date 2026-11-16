from typing import ClassVar

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.auths.constants import USER_FIRST_NAME_MAX_LENGTH, USER_LAST_NAME_MAX_LENGTH
from apps.auths.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email: models.EmailField = models.EmailField(
        unique=True,
        verbose_name="email address",
    )
    first_name: models.CharField = models.CharField(
        max_length=USER_FIRST_NAME_MAX_LENGTH,
        verbose_name="first name",
    )
    last_name: models.CharField = models.CharField(
        max_length=USER_LAST_NAME_MAX_LENGTH,
        verbose_name="last name",
    )
    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="active status",
    )
    is_staff: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="staff status",
    )

    objects: UserManager = UserManager()

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        return self.first_name
