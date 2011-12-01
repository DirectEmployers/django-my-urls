from django.conf.urls.defaults import *
from django.conf import settings
from example.views import MyUrlsList, create_myurl

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^create/?P<url>/$', 'views.create_myurl'),
    (r'^list$', MyUrlsList.as_view()),
)

urlpatterns = urlpatterns + patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    ) if settings.DEBUG else urlpatterson

