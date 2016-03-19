from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
#import pytest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(2)

	def tearDown(self):
		print "Finalizing %s browser ('%s') pointed at URL '%s'" % (self.browser.name, self.browser.title, self.browser.current_url)
		self.browser.quit()
	
	def test_start_list_retrieve_later(self):

		#user goes to homepage
		self.browser.get('http://localhost:8002')

		#user sees "To-Do" in page title and header
		self.assertIn('To-Do', self.browser.title)	
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#user is invited to enter a todo item right away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do-item')

		#user types "buy feathers" into a text box
		inputbox.send_keys('buy feathers')

		import time
		time.sleep(5)

		#when user hits enter, page updates - now shows "1: buy feathers" as item in a todo list table
		inputbox.send_keys(Keys.ENTER)

		import time
		time.sleep(5)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')

		import time
		time.sleep(5)

		self.assertTrue(any(row.text == '1: buy feathers' for row in rows), "New to-do item did not appear in rows")

		#a text box invites user to add a new item 
		self.fail('Finish the test!')

		#user enters "use feathers to make a fly"fly

		#page updates again, now shows both items in list

		#user sees that the site has generated a unique URL for list

		#user visits that URL -- todo list is still there

		#user leaves

		self.fail('Finish the test!')


if __name__ == '__main__':
	unittest.main()
