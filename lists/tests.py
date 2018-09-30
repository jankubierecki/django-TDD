from django.test import TestCase
from .views import home_page
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from .models import Item

from django.template.loader import render_to_string


class HomePageTestCase(TestCase):

    def test_root_url_resolves_home_page(self):

        # When
        found = resolve('/')

        # Then
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):

        # Given
        request = HttpRequest()

        # When
        response = home_page(request)
        expected_html = render_to_string('home.html', request=request)

        # Then
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_handles_POST_request(self):

        # Given
        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_item'] = 'New list element'

        # When
        response = home_page(request)

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'New list element'},
            request=request
        )

        # Then
        self.assertIn('New list element', response.content.decode())
        self.assertEqual(response.content.decode(), expected_html)


class ItemModelTestCase(TestCase):

    def test_saving_and_retrieving_items(self):

        # Given
        first_item = Item()
        second_item = Item()
        first_item.text = 'First item in list'
        second_item.text = 'Second item in list'

        # When
        first_item.save()
        second_item.save()

        saved_items = Item.objects.all()
        first_saved_item, second_saved_item = saved_items[0], saved_items[1]

        # Then
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(first_saved_item.text, 'First item in list')
        self.assertEqual(second_saved_item.text, 'Second item in list')
