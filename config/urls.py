from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import webapp.views

# Examples:
# url(r'^$', 'config.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', webapp.views.index, name='index'),
    # url(r'^db', webapp.views.db, name='db'),
    path('admin/', admin.site.urls),
]
