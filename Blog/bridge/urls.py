"""Bridge URL Configuration

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
from django.contrib import admin

# from blog.views import index, view_post, view_category


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', index),
    # url(r'^blog/view/(?P<slug>[^\.]+).html', 
    # view_post, name='view_blog_post'),
    # url(r'^blog/category/(?P<slug>[^\.]+).html', 
    # view_category, name='view_blog_category'),
]
