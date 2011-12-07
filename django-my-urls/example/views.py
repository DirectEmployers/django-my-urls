from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, FormView
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from myurls.models import Click, MyUrl

def api_create_myurl(request, url='', utm_source=None, utm_medium=None, utm_campaign=None):
    """View that allows creation of short URLs using GET vars.  
    
    This is probably *not* a good idea to put in the wild on the internet.
    """
    
    if request.method=='GET':
        try:
            referrer = request.META['HTTP_REFERRER']
        except:
            referrer = ''

        myurl = MyUrl(to_url=url,
                      from_url=referrer,
                      utm_source=utm_source, 
                      utm_medium=utm_medium,
                      utm_campaign=utm_campaign)
        try:
            myurl.save()
        except:
            HttpResponse("Failed to create Short URL", mimetype="text/plain", status=400)
    else:
        return HttpResponse("Bad Request", status=400)
    # Send the user the short URL
    return HttpResponse(myurl.short_url)

class MyUrlsList(ListView):
    """implements end user view of short url history"""
    context_object_name = "Url"
    model =  MyUrl
    
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #return super(ProtectedView, self).dispatch(*args.**kwargs)
    
#class MyUrlsDetail(DetailView):
    #"""implements end user detail view of short url"""

    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
        #return super(ProtectedView, self).dispatch(*args.**kwargs)

#class EditURLDetail(FormView):
    #"""implements end user edit view for short url"""
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
        #return super(ProtectedView, self).dispatch(*args.**kwargs)
