from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ProfileScreenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alex@example.com",
            email="alex@example.com",
            password="safe-password-123",
            first_name="Alex",
            last_name="Lee",
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_settings_updates_the_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("user_settings"),
            {"first_name": "Alexis", "last_name": "Lee", "email": "alexis@example.com"},
        )
        self.assertRedirects(response, reverse("user_settings"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "alexis@example.com")
        self.assertEqual(self.user.username, "alexis@example.com")
