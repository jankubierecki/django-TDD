from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest


class HomePageTestCase(TestCase):

    def test_root_url_resolves_home_page(self):
        """ tests url  main page routing """

        # When
        found = resolve('/')

        # Then
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):

        # Given
        request = HttpRequest()

        # When
        response = home_page(request)

        # Then
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>TODO Lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
