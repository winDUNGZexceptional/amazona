from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^user/register/$', views.register, name='register'),
	url(r'^user/login/$', views.login, name='login'),
	url(r'^user/logout/$', views.logout, name='logout'),
	url(r'^user/(?P<user_id>[0-9]+)/$', views.show_user, name='show'),
]