from django.conf.urls.defaults import *
from myurls.views import ListView

urlpatterns = patterns('',
    #url(r'/list',views.MyUrlsList.as_view()),
    url(r'^$', 'views.index', name='index'),
    )