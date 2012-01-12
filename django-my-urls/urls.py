# urls.py
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from myurls.models import MyUrl, Click

from example.views import MyUrlsList, api_create_myurl
from example.forms import CreateMyUrlForm, EditMyUrlForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^create/', CreateView.as_view(model=MyUrl,form_class=CreateMyUrlForm)),
    (r'^^edit/(?P<pk>\d+)$', 
        login_required(UpdateView.as_view(model=MyUrl, form_class=EditMyUrlForm))),
    (r'^api/(?P<url>.*)', api_create_myurl),
    (r'^list$', ListView.as_view(model=MyUrl)),
    (r'^history$', ListView.as_view(model=Click)),
)

urlpatterns = urlpatterns + patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    ) if settings.DEBUG else urlpatterson

