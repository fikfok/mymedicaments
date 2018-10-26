from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from mymedicaments import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(template_name='registration/login.html'), name="login"),
    url(r'^logout/$', LogoutView.as_view(template_name='registration/logout.html'), name="logout"),
    url(r'^$', views.home, name='home'),
    url(r'^api/get_medicaments/$', views.get_medicaments, name='get_medicaments'),
    url(r'^api/save_medicament/$', views.save_medicament, name='save_medicament'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
