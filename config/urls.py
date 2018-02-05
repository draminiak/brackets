from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

import webapp.views

# Examples:
# url(r'^$', 'config.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', webapp.views.index, name='index'),
    url(r'^register/$', webapp.views.register, name="register"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^account/$', webapp.views.account, name='account'),
    # url(r'^db', webapp.views.db, name='db'),
    path('admin/', admin.site.urls),
]
