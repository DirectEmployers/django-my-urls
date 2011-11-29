from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, FormView
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.sites.models import Site
from myurls.models import MyUrl, Click

def do_click(response, path):
    """takes a request, finds a MyUrl or raises a 404"""
    if request.method == "GET":
        # see if we have a match if not, 404!
        try:
            myurl = MyUrl.objects.get(short_path__iexact=path)
        except:
            raise Http404
        # We have a match, so save click data and redirect
        click = Click(myurl=myurl,
                      destination_url=myurl.destination_url,
                      redirect_url=myurl.redirect_url,
                      referrer_domain=request.META.HTTP_REMOTE_HOST,
                      referrer_url=request.META.HTTP_REFERRER,
                      site=Site.objects.get_current(),
                      user=request.user,
                      user_ip=request.META.HTTP_HOST,
                      user_language=request.META.HTTP_ACCEPT_LANGUAGE,
                      user_agent=request.META.HTTP_USER_AGENT)
        click.save()
        # do the redirect
        HttpResponseRedirect(myurl.redirect_url)