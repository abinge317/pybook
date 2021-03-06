"""PyBook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from PyBook.views import *
from django.views.generic.base import RedirectView
urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url('^hello/$', hello),
    url(r'^books/$', show_books),
    url(r'^books/(.+)/(\d+)/$', show_books),
    url('^time/$', current_time),
    url(r'time/plus/(\d{1,2})/$', time_ahead),
    url(r'^favicon\.ico$', RedirectView.as_view(url = r'static/favicon.ico')),

]
