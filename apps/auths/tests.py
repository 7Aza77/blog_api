from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CustomUserModelTests(TestCase):
    def test_create_user_successful(self) -> None:
        email: str = "TestUser@Example.COM"
        password: str = "securepassword123"
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name="Test",
            last_name="User",
        )

        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password123")

    def test_create_superuser_successful(self) -> None:
        email: str = "admin@example.com"
        password: str = "adminpassword123"
        superuser = User.objects.create_superuser(
            email=email,
            password=password,
            first_name="Admin",
            last_name="Root",
        )

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_invalid_staff_flags(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin2@example.com",
                password="password123",
                is_staff=False,
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin3@example.com",
                password="password123",
                is_superuser=False,
            )

    def test_user_string_representation(self) -> None:
        user = User(email="author@example.com", first_name="John", last_name="Doe")
        self.assertEqual(str(user), "author@example.com")
        self.assertEqual(user.get_full_name(), "John Doe")
        self.assertEqual(user.get_short_name(), "John")
