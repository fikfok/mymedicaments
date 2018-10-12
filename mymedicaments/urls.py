from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from mymedicaments import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^$', views.home, name='home'),
]
