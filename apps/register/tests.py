from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationDatabaseTests(TestCase):
    def test_registration_creates_a_user_with_a_hashed_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Test",
                "last_name": "Student",
                "email": "test.student@example.com",
                "password": "safe-password-123",
            },
        )

        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="test.student@example.com")
        self.assertEqual(user.email, "test.student@example.com")
        self.assertTrue(user.check_password("safe-password-123"))
        self.assertNotEqual(user.password, "safe-password-123")
