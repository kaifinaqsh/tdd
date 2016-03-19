import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from lists.models import Item, List
#import pytest


#class NewVisitorTest(unittest.TestCase):
#class NewVisitorTest(LiveServerTestCase):

class NewVisitorTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownCLass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(2)

	def tearDown(self):
		print "Finalizing %s browser ('%s') pointed at URL '%s'" % (self.browser.name, self.browser.title, self.browser.current_url)
		Item.objects.filter().delete()
		List.objects.filter().delete()
		self.browser.refresh()
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		# (find table in newly-displayed page)
		# (find table's rows to be searched)
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
	

	def test_start_list_retrieve_later(self):

		#user goes to homepage
		self.browser.get('http://localhost:8002')
#		self.browser.get(self.live_server_url)

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
		time.sleep(1)

		#when user hits enter, taken to new URL - 
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegexpMatches(edith_list_url, '/lists/.+')

		#now page shows "1: buy feathers" as an item in a todo list table

		time.sleep(1)

		#check for row text in row table
		self.check_for_row_in_list_table('1: buy feathers')

#		self.assertTrue(any(row.text == '1: buy feathers' for row in rows), "New to-do item did not appear in rows")

		#user enters "use feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('use feathers to make a fly')

		time.sleep(1)

		inputbox.send_keys(Keys.ENTER)

		time.sleep(1)

		#page updates again, now shows both items in list

		#again, check for row text in row table
		self.check_for_row_in_list_table('2: use feathers to make a fly')
		self.check_for_row_in_list_table('1: buy feathers')

		#a new user, Francis, visits site

		##use a new browser session to make sure none of Edith's info is coming through
		##from cookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()

		#Francis visits home page - no sign of Edith's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('buy feathers', page_text)
		self.assertNotIn('user feathers to make a fly', page_text)

		#Francis starts a new list by entering a new item - 
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('buy milk')
		inputbox.send_keys(Keys.ENTER)

		#Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegexpMatches(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#again, nothing from Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('buy feathers', page_text)
		self.assertIn('buy milk', page_text)

#		#user wonders if site will remember her list
#		#user sees that the site has generated a unique URL for list
#		#with explanatory text about it
#
#		#user visits that URL -- todo list is still there
#
#		#user leaves

		self.fail('Finish the test!')



	def test_layout_and_styling(self):
		# Edith goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# notices input box is centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		ib_width = inputbox.size['width']
		ib_x = inputbox.location['x']
		ib_middle = ib_x + ib_width / 2
		self.assertAlmostEqual(ib_middle, 512, delta=5)

		# starts a new list and sees input centered there, too
		# send_keys text and enter
		# resulting inputbox is also centered
		inputbox.send_keys('testing \n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		ib_x = inputbox.location['x']
		ib_width = inputbox.size['width']
		ib_middle = ib_x + ib_width / 2
		self.assertAlmostEqual(ib_middle, 512, delta=5)


		




#if __name__ == '__main__':
#	unittest.main()
