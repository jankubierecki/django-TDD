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

    def test_home_page_only_saves_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):
    def test_saving_POST_request(self):

        # When
        self.client.post('/lists/new', data={'new_item': 'New list element'})

        new_item = Item.objects.first()

        # Then
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(new_item.text, 'New list element')

    def test_redirects_after_POST(self):

        # When
        response = self.client.post(
            '/lists/new',
            data={'new_item': 'New list element'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],
                         '/lists/the-only-list-in-the-world/')
