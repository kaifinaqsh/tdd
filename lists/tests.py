#from django.http import JsonResponse
#from django.shortcuts import render
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
from lists.models import Item, List

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


#	def test_home_page_only_saves_items_when_necessary(self):
#		new_list_item_text = 'A new list item'
#		(request, rc) = self.setup_request(new_list_item_text, '')
#
#		response = home_page(request)
#
#		self.assertEqual(Item.objects.count(), 0)



class ListAndItemModelsTest(TestCase):
	
	def test_saving_and_retrieving_items(self):

		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'first ever item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'second item\'s text'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'first ever item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'second item\'s text')
		self.assertEqual(second_saved_item.list, list_)



class ListViewTest(TestCase):

	def setup_request(self, new_text, request_type='POST'):
		request = HttpRequest()
		request.method = request_type
		if request_type == 'POST':
			request.POST['item_text'] = new_text
		rc = RequestContext(request)
		rc.push({'new_item_text': new_text})
		return (request, rc)


	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_only_items_for_that_list(self):
#		new_list_item_text = 'A new list item'
#		(request, rc) = self.setup_request(new_list_item_text, '')

		rightlist_ = List.objects.create()
		Item.objects.create(text='right list 1', list=rightlist_)
		Item.objects.create(text='right list 2', list=rightlist_)
		otherlist_ = List.objects.create()
		Item.objects.create(text='other list 1', list=otherlist_)
		Item.objects.create(text='other list 2', list=otherlist_)

		response = self.client.get('/lists/%d/' % (rightlist_.id,))

		self.assertContains(response, 'right list 1')
		self.assertContains(response, 'right list 2')
		self.assertNotContains(response, 'other list 1')
		self.assertNotContains(response, 'other list 2')


	def test_passes_right_list_to_template(self):
		# create other list
		other_list = List.objects.create()
		# create right list
		right_list = List.objects.create()
		# get page from /lists/%d/ using right list
		response = self.client.get('/lists/%d/' % (right_list.id,))
		# assert that response's list = right list
		self.assertEqual(response.context['list'], right_list)


class NewListTest(TestCase):

	def setup_request(self, new_text, request_type='POST'):
		request = HttpRequest()
		request.method = request_type
		if request_type == 'POST':
			request.POST['item_text'] = new_text
		rc = RequestContext(request)
		rc.push({'new_item_text': new_text})
		return (request, rc)


	def test_saving_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

#		new_list_item_text = 'A new list item'
#		(request, rc) = self.setup_request(new_list_item_text, 'POST')
#
#		response = home_page(request)
#
#		self.assertEqual(Item.objects.count(), 1)
#		new_item = Item.objects.first()
#		self.assertEqual(new_item.text, new_list_item_text)


	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

		new_list = List.objects.first()

		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

#		self.assertEqual(response.status_code, 302)
#		self.assertEqual(response['location'], '/lists/only-list-in-the-world/')

#		new_list_item_text = 'A new list item'
#		(request, rc) = self.setup_request(new_list_item_text, 'POST')
#
#		response = home_page(request)
#
#		self.assertEqual(response.status_code, 302)
#		self.assertEqual(response['location'], '/lists/only-list-in-the-world/')



class NewItemTest(TestCase):

	def test_can_save_POST_request_to_existing_list(self):

		right_list = List.objects.create()
		other_list = List.objects.create()

		# post new item for existing list (right_list) - and using new URL /lists/n/additem
		self.client.post('/lists/%d/add_item' % (right_list.id,), data={'item_text': 'new item for existing list'})

		# created 1 item (with "right_list")
		self.assertEqual(Item.objects.count(), 1)

		#get latest item
		new_item = Item.objects.first()

		#item's list = "right_list"
		self.assertEqual(new_item.list, right_list)
		self.assertNotEqual(new_item.list, other_list)
		#item's text = entered text
		self.assertEqual(new_item.text, 'new item for existing list')


	def test_add_to_existing_list_redirects_to_list_view(self):

		# create new right list
		right_list = List.objects.create()
		# create new other list
		other_list = List.objects.create()
		# do post - with response = client.post (add-URL, data)
		response = self.client.post('/lists/%d/add_item' % (right_list.id,), data={'item_text': 'new item for existing list'})
		# test assertRedirects (response, list-view URL, right list)
		self.assertRedirects(response, '/lists/%d/' % (right_list.id,))

