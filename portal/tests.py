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

    def _login_client(self):
        Parent.objects.create_user(
            username="test@gmail.com", password="testpassword")
        login_successful = self.client.login(
            username="test@gmail.com", password="testpassword")
        self.assertTrue(login_successful)

    def test_login_GET_parent(self):
        self._login_client()
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
        self._login_client()
        response = self.client.get(reverse("choose"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portal/choose.html")

    def test_dashboard(self):
        self._login_client()
        response = self.client.get(
            reverse("dashboard", kwargs={"id": "STU-0225"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portal/dashboard.html")

    def test_dashboard_wrongchild(self):
        self._login_client()
        response = self.client.get(
            reverse("dashboard", kwargs={"id": "STU-0226"}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("choose"))

    def test_statement(self):
        self._login_client()
        response = self.client.get(
            reverse("statement", kwargs={"id": "STU-0225"}))
        self.assertEqual(response.status_code, 200)

    def test_statement_print(self):
        self._login_client()
        response = self.client.get(
            reverse("statement_print", kwargs={"id": "STU-0225"}))
        self.assertEqual(response.status_code, 200)

    def test_invite_GET(self):
        self._login_client()
        response = self.client.get(
            reverse("invite", kwargs={"id": "STU-0225"}))
        self.assertEqual(response.status_code, 200)

    def test_invite_wrongchild(self):
        self._login_client()
        response = self.client.get(
            reverse("invite", kwargs={"id": "STU-0226"}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("choose"))

    def test_invite_POST(self):
        self._login_client()
        response = self.client.post(
            reverse("invite", kwargs={"id": "STU-0225"}), data={"email": "test@gmail.com"})
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "portal/invite.html")
        self.assertIn("message", response.context)
        self.assertTrue(response.context.get("message"))

    def test_sendmail_GET(self):
        self._login_client()
        response = self.client.get(reverse("proceed"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "portal/proceed.html")

    def test_sendmail_POST(self):
        self._login_client()
        response = self.client.post(reverse("proceed"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "portal/proceed.html")
        self.assertIn("message", response.context)
        self.assertEqual(response.context["message"], "Email Sent")

    def test_contact(self):
        response = self.client.get(reverse("contact"))
        self.assertTrue(200, response.status_code)
        self.assertTemplateUsed(response, "portal/contact.html")

    def test_contactus(self):
        response = self.client.get(reverse("contact_us"))
        self.assertTrue(200, response.status_code)
        self.assertTemplateUsed(response, "portal/contact_us.html")

    def test_logout(self):
        self._login_client
        response = self.client.get(reverse("logout"))
        self.assertTrue(302, response.status_code)
        self.assertRedirects(response, reverse("logged_out"))

    def test_logged_out(self):
        response = self.client.get(reverse("logged_out"))
        self.assertTrue(200, response.status_code)
        self.assertTemplateUsed(response, "portal/logged_out.html")
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_pay_GET(self):
        response = self.client.get(reverse("pay", kwargs={"id":"STU-0225"}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "portal/pay.html")


# Create your tests here.
