from django import http
from django.conf import settings

from myurls.models import MyUrl

class MyUrlsFallbackMiddleware(object):
    """Checks for short URL and redirects on 404s"""
       
    def process_response(self, request, response):
        """Accepts a Django request and redirects to a matching myurl"""
        if response.status_code != 404:
            return response
        path = request.get_full_path()[1:]
        # get the myurl - even if someone appends a trailing /
        if path.endswith('/'):
            try:
                myurl = MyUrl(site__id__exact=settings.SITE_ID,
                              short_path=path[:path.rfind('/')]+path[path.rfind('/')+1:])
            except MyUrl.DoesNotExist:
                return response
        else:
            try:
                myurl = MyUrl.objects.get(short_url__exact=request.path)
            except MyUrl.DoesNotExist:
                return response
                # need to put somethign here for failed clicks.
        # Makes sure we are not redirecting to nowhere
        if myurl is not None:
            if myurl.redirect_url == '':
                return http.HttpResponseGone()
        else:
            # create and save the click history
            click = Click(myurl=myurl,
                          to_url=myurl.to_url,
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
            if myurl.redirect_type == '301':
                return http.HttpResponsePermanentRedirect(myurl.redirect_url)
            else:
                return http.HttpResponseRedirect(myurl.redirect_url)
            # No MyUrl was found. Let Django deal with it.
        return response
