from django.test import TestCase
from .views import home_page
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from .models import Item, List

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


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):

        # When

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "First item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()

        saved_items = Item.objects.all()
        first_saved_item, second_saved_item = saved_items[0], saved_items[1]

        # Then
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.list, list_)
        self.assertEqual(first_saved_item.text, "First item")
        self.assertEqual(second_saved_item.text, "Second item")

        self.assertEqual(saved_list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):

        # Given
        list_ = List.objects.create()

        # When
        response = self.client.get('/lists/%d/' % (list_.id,))

        # Then
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_items_for_particular_list(self):

        # Given
        list_correct = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_correct)
        Item.objects.create(text='itemey 2', list=list_correct)

        list_other = List.objects.create()
        Item.objects.create(text='itemey 1 of other list', list=list_other)
        Item.objects.create(text='itemey 2 of other list', list=list_other)

        # When
        response = self.client.get('/lists/%d/' % (list_correct.id,))

        # Then
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

        self.assertNotContains(response, 'itemey 1 of other list')
        self.assertNotContains(response, 'itemey 2 of other list')

    def test_passes_correct_list_to_template(self):

        # Given
        other_list = List.objects.create()
        correct_list = List.objects.create()

        # When
        response = self.client.post(
            '/lists/%d/' % (correct_list.id,))

        # Then
        self.assertEqual(response.context['list'], correct_list)


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

        list_new = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (list_new.id,))


class NewItemInListTest(TestCase):

    def test_can_save_POST_request_to_existing_list(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        # When
        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'new_item': 'New item for an existing list'}
        )

        new_item = Item.objects.first()

        # Then
        self.assertEqual(Item.objects.count(), 1)

        self.assertEqual(new_item.text, 'New item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        # When
        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'new_item': 'New item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
