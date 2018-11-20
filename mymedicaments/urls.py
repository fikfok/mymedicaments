from django.conf.urls import url
from django.contrib import admin
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
    url(r'^api/get_medicament_data/(?P<medicament_id>[0-9]+)$', views.get_medicament_data, name='get_medicament_data'),
    url(r'^api/save_medicament/$', views.save_medicament, name='save_medicament'),
    url(r'^api/get_categories/$', views.get_categories, name='get_categories'),
    url(r'^api/update_medicament/(?P<medicament_id>[0-9]+)$', views.update_medicament, name='update_medicament'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
