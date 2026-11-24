from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginScreenTests(TestCase):
    def test_valid_login_redirects_to_profile(self):
        User.objects.create_user(
            username="student@example.com",
            email="student@example.com",
            password="safe-password-123",
            first_name="Student",
        )

        response = self.client.post(
            reverse("login"),
            {"email": "student@example.com", "password": "safe-password-123"},
        )

        self.assertRedirects(response, reverse("profile"))


class LogoutTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_user("a@b.c", "a@b.c", "pw12345678")
        self.client.login(username="a@b.c", password="pw12345678")

    def test_post_logs_out_and_redirects_home(self):
        response = self.client.post("/login/logout/")
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(self.client.get("/profile/").status_code, 302)  # protected again

    def test_get_is_not_allowed(self):
        self.assertEqual(self.client.get("/login/logout/").status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)  # still logged in
