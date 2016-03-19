from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.template.loader import get_template
from django.template import RequestContext

from lists.models import Item


#settings.configure()

def home_page(request):

#	rc = RequestContext(request)
#	rc.push({'new_item_text': request.POST.get('new_item_text', ''),})


	if request.method == 'POST':
		new_item_text = request.POST['item_text']
		Item.objects.create(text=new_item_text)
		return redirect('/lists/only-list-in-the-world/')
	else:
		new_item_text = ''

	items = Item.objects.all()

	rc = RequestContext(request)
	rc.push({'items': items})

#	return render(request, 'home.html', {'items': items})

	return render(request, 'home.html', rc)


#	rc = RequestContext(request)
#	rc.push({'new_item_text': new_item_text})
#
#	return render(request, 
#			'home.html', 
#			{'new_item_text': new_item_text})

#	return render(request, 
#			'home.html', 
#			rc)



#	response = home_page(request)

#	item = Item()
#	item.text = request.POST.get('item_text', '')
#	item.save()

#	return render(request, 
#			'home.html', 
#			rc)


def view_list(request):

	items = Item.objects.all()

	rc = RequestContext(request)
	rc.push({'items': items})

#	return render(request, 'home.html', {'items': items})

	return render(request, 'home.html', rc)
