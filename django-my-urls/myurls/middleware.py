from django import http
from django.conf import settings

from myurls.models import MyUrl, Click

class MyUrlsFallbackMiddleware(object):
    """Checks for short URL and redirects on 404s"""
       
    def process_response(self, request, response):
        """Accepts a Django request and redirects to a matching myurl"""
        if response.status_code != 404:
            return response
        # remove / from front of URL
        path = request.get_full_path()[1:]
        # get the myurl - even if someone appends a trailing /
        if path.endswith('/'):
            try:
                myurl = MyUrl.objects.get(
                    short_path__exact=path[:path.rfind('/')]+path[path.rfind('/')+1:])
            except MyUrl.DoesNotExist:                
                myurl=None
        else:
            try:
                myurl = MyUrl.objects.get(short_path__exact=path)
            except MyUrl.DoesNotExist:
                myurl=None
                # need to put somethign here for failed clicks.
        # see if myurl is defined
        # Makes sure we are not redirecting to nowhere
        if myurl is None:
                return http.HttpResponseGone()
        
        else:
            # create and save the click history
            user = None if request.user.is_anonymous else request.user
            # Store HTTP headers if we have them
            try:
                referrer_url = request.META.HTTP_REFERRER
            except AttributeError:
                referrer_url = None
            try:
                user_domain = request.META.REMOTE_HOST
            except AttributeError:
                user_domain = None
            try:
                user_language = request.META.HTTP_ACCEPT_LANGUAGE
            except AttributeError:
                user_language = None
            try:
                user_agent = request.META.HTTP_USER_AGENT
            except AttributeError:
                user_agent = None
            try:
                user_ip = request.META.REMOTE_ADDR
            except AttributeError:
                user_ip = None
            click = Click(myurl=myurl,
                          to_url=myurl.to_url,
                          redirect_url=myurl.redirect_url,
                          user_domain=user_domain,
                          referrer_url=referrer_url,
                          site_id=settings.SITE_ID,
                          user=user,
                          user_ip=user_ip,
                          user_language=user_language,
                          user_agent=user_agent)
            click.save()
            # do the redirect
            if myurl.redirect_type == '301':
                return http.HttpResponsePermanentRedirect(myurl.redirect_url)
            else:
                return http.HttpResponseRedirect(myurl.redirect_url)
            # No MyUrl was found. Let Django deal with it.
        return response
