"""CSE_442 URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import settings
from django.conf.urls.static import static
from project import views

#Connecting all pages together, urls directs towards views--which are our html python coded pages. 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login_user$', views.login_user, name='login_user'),
    url(r'^logout_view$', views.logout_view, name='logout_view'),
    url(r'^aboutus$', views.aboutus, name='aboutus'),
    url(r'^register$', views.register, name='register'),
    url(r'^check_register', views.check_register, name='check_register'),
    url(r'^course_list$', views.course_list, name='course_list'),
    url(r'^file_upload$', views.file_upload, name='file_upload'),
    url(r'^upvote/(?P<file_chosen>.*)$', views.upvote, name='upvote'),
    url(r'^my_uploads$', views.my_uploads, name='my_uploads'),
    url(r'^my_downloads$', views.my_downloads, name='my_downloads'),
    url(r'^download/(?P<file_chosen>.*)$', views.download, name='download'),
    url(r'^(?P<identity>[0-9a-zA-Z]+)/course_view/$', views.course_view, name='course_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
