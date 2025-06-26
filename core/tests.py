from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.forms import CustomUserCreationForm

User = get_user_model()


class CoreViewsTest(TestCase):

    def setUp(self):
        """Set up test client and a sample user"""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

    def test_register_view_GET(self):
        """Test GET request for the registration page"""
        response = self.client.get(reverse("core:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/register.html")

    def test_register_view_POST_valid(self):
        """Test successful user registration"""
        response = self.client.post(reverse("core:register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!"
        })
        self.assertEqual(User.objects.count(), 2)  # New user should be created
        self.assertRedirects(response, reverse("core:home"))  # Redirect after successful signup

    def test_register_view_POST_invalid(self):
        """Test failed registration due to mismatched passwords"""
        response = self.client.post(reverse("core:register"), {
            "username": "failuser2",
            "email": "fail2@example.com",
            "password1": "password1243",
            "password2": "password456"  # Mismatched passwords
        })
        self.assertEqual(User.objects.count(), 1)  # No new user created
        #self.assertContains(response, "password fields didn’t match")  # Error message

    def test_edit_profile_view_GET(self):
        """Test GET request for profile editing page (authenticated user)"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("core:edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/edit_profile.html")

    def test_edit_profile_view_POST(self):
        """Test successful profile update"""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("core:edit_profile"), {
            "social_links": ["https://github.com/testuser"]
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.social_links, ["https://github.com/testuser"])
        self.assertRedirects(response, reverse("core:profile"))

    def test_profile_view_requires_login(self):
        """Test profile page requires authentication"""
        response = self.client.get(reverse("core:profile"))
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_user_profile_view_GET(self):
        """Test viewing another user's profile"""
        response = self.client.get(reverse("core:user_profile", args=["testuser"]))
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, "core/profile.html")

    def test_landing_page_view_GET(self):
        """Test landing page loads successfully"""
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/landing.html")

    def test_logout_view(self):
        """Test user logout functionality"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("core:logout"))
        self.assertRedirects(response, reverse("core:home"))
