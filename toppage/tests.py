from django.test import TestCase, Client


class RedirectTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirect(self):
        response = self.client.get("")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/core/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
