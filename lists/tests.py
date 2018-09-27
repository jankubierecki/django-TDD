from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

from django.template.loader import render_to_string


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
        response = home_page(request)

        # When
        result_html = render_to_string('home.html')

        # Then
        self.assertTrue(response.content.strip().endswith(b'</html>'))
