from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class HomePageTestCase(TestCase):

    def test_root_url_resolves_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
