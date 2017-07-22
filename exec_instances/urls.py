from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'exec_instances'
urlpatterns = [
	url(r'^$', views.exec_instances, name='exec_instances'),
	url(r'^upload/$', views.upload, name = 'upload'),
]
