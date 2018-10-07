from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_if_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retieve_later(self):

        # user wants to play with todoapp so he is heading to main page
        self.browser.get(self.live_server_url)

        # user has noticed that main page and header title has word 'Lists'
        # in its header
        self.assertIn('Lists', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('Lists', header_text)

        # user noticed text area field with placeholder
        input_box = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(input_box.get_attribute(
            'placeholder'), 'Enter your task!')

        # in the text area user has put 'buy Peacock feathers'
        input_box.send_keys('buy Peacock feathers')

        # after user pressed enter button, the list got updated and now it
        # contains the above user's thing to do
        input_box.send_keys(Keys.ENTER)

        self.check_if_row_in_table('1: buy Peacock feathers')

        # on the main page there is still text area field that can accept
        # another user's thing to do
        # the user wrote 'use peacock feathers as a component of a bait
        # recipie' as a next thing do to in the text area
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(
            'use peacock feathers as a component of a bait recipie')
        input_box.send_keys(Keys.ENTER)

        self.check_if_row_in_table(
            '2: use peacock feathers as a component of a bait recipie')

        # the page has been updated again, and now it displays two user's works
        self.fail('Test has ended')

        # the user has wondered if the list is capable of remembering his list.
        # The user noticed the unique generated URL adress next to which
        # is a text with explanation

        # user clicks the link and gets transformed to another page that
        # displays his list

        # fully-satisfied user goes to bed
