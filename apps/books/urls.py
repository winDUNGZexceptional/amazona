from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.book_list, name='list'),
	url(r'^add/$', views.add_book, name='add'),
	url(r'^create/$', views.create_book, name='create'),
	url(r'^(?P<book_id>[0-9]+)/$', views.show_book, name='show'),
	url(r'^(?P<book_id>[0-9]+)/review/create/$', views.add_review, name='add_review'),
	url(r'^(?P<book_id>[0-9]+)/review/(?P<review_id>[0-9]+)/$', views.delete_review, name='delete_review'),
]