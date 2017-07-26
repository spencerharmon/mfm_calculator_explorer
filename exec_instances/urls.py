from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'exec_instances'
urlpatterns = [
	url(r'^$', views.exec_instances, name='exec_instances',kwargs = {'error_message': None}),
	url(r'^upload/$', views.upload, name = 'upload'),
	url(r'^(?P<instance_name>[\w]+)/$', views.instance_detail, name = 'instance_detail', kwargs = {'error_message': None}),
	url(r'^(?P<instance_name>[\w]+)/(?P<aeps_name>[\w]+)/$', views.aeps_detail, name = 'aeps_detail',kwargs = {'error_message': None}),
	url(r'^(?P<instance_name>[\w]+)/(?P<aeps_name>[\w]+)/(?P<site_id>[\w]+)/$', views.site_detail, name = 'site_detail',kwargs = {'error_message': None})
]
