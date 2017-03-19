from django.conf.urls import url

from .views import (
	posts_create,
	posts_update,
	posts_detail,
	posts_list,
	posts_delete,)



urlpatterns = [
    url(r'^create/$', posts_create, name='list'),
    url(r'^(?P<id>\d+)/$', posts_detail, name='detail'),
    url(r'^$', posts_list),
    url(r'^(?P<id>\d+)/edit/$', posts_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', posts_delete),
]
