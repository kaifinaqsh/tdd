#import pytest
#import pytest_django


#from django.http import JsonResponse
#from django.shortcuts import render
#from django.template import RequestContext
#from django.views.decorators.csrf import csrf_exempt
#
#import jsonpickle
#
#from rest_framework import viewsets
##from lists.helpers import suds_to_json
##from lists.models import App, Endpoint
##from lists.serializers import AppSerializer, EndpointSerializer
#from suds.client import Client

#from lists.helpers import SudsWrapper

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.template import RequestContext
from django.apps import AppConfig

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):

	def setup_request(self, new_text, request_type='POST'):
		request = HttpRequest()
		request.method = request_type
		if request_type == 'POST':
			request.POST['item_text'] = new_text
		rc = RequestContext(request)
		rc.push({'new_item_text': new_text})
		return (request, rc)


	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)


	def test_home_page_returns_right_html(self):
		new_list_item_text = 'A new list item'
		(request, rc) = self.setup_request(new_list_item_text, 'POST')

		response = home_page(request)

#		expected_html = render_to_string('home.html', rc)
##		expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
#
#		self.assertEqual(response.content.decode(), expected_html)


	def test_home_page_can_save_a_POST_request(self):
		new_list_item_text = 'A new list item'
		(request, rc) = self.setup_request(new_list_item_text, 'POST')

		response = home_page(request)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, new_list_item_text)


	def test_home_page_redirects_after_POST(self):
		new_list_item_text = 'A new list item'
		(request, rc) = self.setup_request(new_list_item_text, 'POST')

		response = home_page(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/only-list-in-the-world/')

#		self.assertIn(new_list_item_text, response.content.decode())
#		expected_html = render_to_string( 'home.html', rc )
##		expected_html = render_to_string( 'home.html', {'new_item_text': 'A new list item'} )
#		self.assertEqual(response.content.decode(), expected_html)


	def test_home_page_only_saves_items_when_necessary(self):
		new_list_item_text = 'A new list item'
		(request, rc) = self.setup_request(new_list_item_text, '')

		response = home_page(request)

		self.assertEqual(Item.objects.count(), 0)


	def test_home_page_displays_all_list_items(self):
		new_list_item_text = 'A new list item'
		(request, rc) = self.setup_request(new_list_item_text, '')

		Item.objects.create(text='item many 1')
		Item.objects.create(text='item many 2')

		response = home_page(request)

		self.assertIn('item many 1', response.content.decode())
		self.assertIn('item many 2', response.content.decode())



class ItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'first ever item'
		first_item.save()

		second_item = Item()
		second_item.text = 'second item\'s text'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'first ever item')
		self.assertEqual(second_saved_item.text, 'second item\'s text')



class ListViewTest(TestCase):

	def setup_request(self, new_text, request_type='POST'):
		request = HttpRequest()
		request.method = request_type
		if request_type == 'POST':
			request.POST['item_text'] = new_text
		rc = RequestContext(request)
		rc.push({'new_item_text': new_text})
		return (request, rc)


	def test_displays_all_items(self):
		new_list_item_text = 'A new list item'
		(request, rc) = self.setup_request(new_list_item_text, '')
#		(request, rc) = self.setup_request(new_list_item_text, request_type='GET')

		Item.objects.create(text='item many 1')
		Item.objects.create(text='item many 2')

		response = self.client.get('/lists/only-list-in-the-world/')

		self.assertContains(response, 'item many 1')
		self.assertContains(response, 'item many 2')

#		response = home_page(request)
#
#		self.assertIn('item many 1', response.content.decode())
#		self.assertIn('item many 2', response.content.decode())





