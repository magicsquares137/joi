from django.urls import reverse, resolve
from django.test import TestCase
from .views import home, character_conversation
from .models import Characters


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve("/")
        self.assertEquals(view.func, home)


class ConvosTests(TestCase):
    def setUp(self):
        Characters.objects.create(name="Django", description="Django board.")

    def test_chars_view_success_status_code(self):
        url = reverse("characters", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_chars_view_not_found_status_code(self):
        url = reverse("characters", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
