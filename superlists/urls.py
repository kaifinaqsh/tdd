"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin
from lists import views as list_views
from lists import urls as list_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'superlists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),

	url(r'^$', list_views.home_page, name='home'),

	url(r'^lists/', include(list_urls)),

#	url(r'^lists/new$', views.new_list, name='new_list'),
#
#	url(r'^lists/(\d+)/$', views.view_list, name='view_list'),
#
#	url(r'^lists/(\d+)/add_item$', views.add_item, name='add_item'),

]
