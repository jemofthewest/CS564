"""CS564 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

# from django.contrib import admin
from readgood.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^books/$', BookList.as_view(), name='books'),
    url(r'^book/(?P<pk>[0-9]+X?)/$', BookDetail.as_view(), name='book_pk'),
    url(r'^book/(?P<slug>[-\w]+)$', BookDetail.as_view(), name='book_slug'),
    url(r'^authors/$', AuthorList.as_view(), name='authors'),
    url(r'^author/(?P<slug>[-\w]+)$', AuthorDetail.as_view(), name='author_detail'),
    url(r'^publishers/$', PublisherList.as_view(), name='publishers'),
    url(r'^publisher/(?P<slug>[-\w]+)$', PublisherDetail.as_view(), name='publisher_detail'),
    url(r'^search/$', search, name='search'),
]
