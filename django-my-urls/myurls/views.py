from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from myurls.models import MyUrl, Click


class MyUrlsList(ListView):
    """implements end user view of short url history"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args.**kwargs)
    
class MyUrlsDetail(DetailView):
    """implements end user detail view of short url"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args.**kwargs)

class EditURLDetail(For
    """implements end user edit view for short url"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args.**kwargs)

