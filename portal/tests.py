from django.test import TestCase, Client
from . models import Parent
from django.urls import reverse


class PortalTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_register_GET(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portal/register.html")

    def test_register_POST_notparent(self):
        credentials = {"email": "nochild@gmail.com",
                       "password": "nochild@gmail.com"}
        response = self.client.post(reverse("register"), credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portal/register.html")
        self.assertIn("message", response.context)
        self.assertEqual(
            response.context["message"], "Email provided is not recognised by the school. Visit school to update!")

    def test_register_POST_existingparent(self):
        Parent.objects.create_user(
            username="existing@gmail.com", password="existing")

        # Attempt to register the user
        credentials = {"email": "existing@gmail.com", "password": "existing"}
        response = self.client.post(reverse("register"), credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portal/register.html")
        self.assertIn("message", response.context)
        self.assertEqual(
            response.context["message"], "The email already exists")

    def test_register_POST_parent(self):
        credentials = {"email": "test@gmail.com", "password": "test@gmail.com"}
        response = self.client.post(reverse("register"), credentials)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertRedirects(response, reverse("choose"))

    def test_login_GET(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portal/login.html")

    # def _login_client
    def _login_client(self):
        Parent.objects.create_user(
            username="test@gmail.com", password="testpassword")
        login_successful = self.client.login(
            username="test@gmail.com", password="testpassword")
        return login_successful

    def test_login_GET_parent(self):
        login_successful = self._login_client()
        self.assertTrue(login_successful)
        self.assertTrue('_auth_user_id' in self.client.session)
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("choose"))

    def test_login_POST(self):
        Parent.objects.create_user(
            username="test@gmail.com", password="testpassword")
        data = {"email": "test@gmail.com", "password": "testpassword"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("choose"))

    def test_unknown_choose(self):
        response = self.client.get(reverse("choose"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=%2F")

    def test_parent_choose(self):
        login_successful = self._login_client()
        self.assertTrue(login_successful)
        response = self.client.get(reverse("choose"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portal/choose.html")





# Create your tests here.
