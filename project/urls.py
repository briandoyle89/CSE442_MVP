from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('', views.index, name='index'),

    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^check_register$', views.check_register, name='check_register'),
    url(r'^course_view$', views.course_view, name='course_view'),
    url(r'^file_upload$', views.file_upload, name='file_upload'),
]