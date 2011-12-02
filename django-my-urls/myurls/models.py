from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from basex import BaseX

class MyUrl(models.Model):
    """Short url model. Domains are pulled from the django.contrib.sites.

    Short URLs are this models PK encoded in baseX using
    settings.SHORTY_CHARACTER_SET.

    Attributes:

    from_site -- Site responsible for creating the shorty
    from_url -- URL responsible for creating the shorty
    to_url -- the destination URL
    short_path -- the short URL's path
    redirect_type -- the type of redirect to return
    notes -- user notes
    created -- creation timestamp
    utm_source -- Google analytics source
    utm_medium -- Google analytics medium
    utm_term -- Google analytics search keyword
    utm_content -- Google analytics content
    utm_campaign -- Google analytics campaign
    append_text -- Extra text to be appended after a & or ? in url
    
    Methods:
    
    save(*args, **kwargs) -- creates short URL and saves to database.
    """

    CHOICES = (
        (_('301 - permanent'), '301'),
        (_('302 - unspecified'), '302'),
        # Right now Django does not support these:
        #(_('303 - see other'), '303'),
        #(_('307 - temporary'), '307'),
        )
    user = models.ForeignKey(User, related_name='short_urls', 
                             null= True, blank=True)
    created = models.DateTimeField(_('Created on'), auto_now_add=True)
    site = models.ForeignKey(Site, related_name="short_urls",
                             default=settings.SITE_ID)
    from_url = models.URLField(_('Source URL'), max_length=200,
        help_text=_('URL where shorty was created'), null=True, blank=True)
    to_url = models.URLField(_('Destination URL'),
        help_text=_('Full URL including scheme (http://, ftp://, etc...'))
    redirect_url = models.URLField(_('URL to send user to'), max_length=300, 
                                 blank=True, null=True)
    short_path = models.CharField(_('Encoded Path'), max_length=10,
                                  blank=True, null=True, db_index=True)
    short_url = models.URLField(_('Short URL'),
                                 db_index=True, null=True, blank=True)
    redirect_type = models.CharField(_('Redirect Type'),
                    max_length=3, choices=CHOICES, 
                    default=settings.MYURLS_DEFAULT_REDIRECT_TYPE)
    notes = models.TextField(_('Notes'), null=True, blank=True)
    created = models.DateTimeField(_('Created Date and Time'),
                                   auto_now_add=True)
    # see Google's URL builder for details on UTM Parameters:
    # http://www.google.com/support/analytics/bin/answer.py?answer=55578    
    utm_source = models.CharField(_('Analytics source'),
                                  max_length=80,
                                  null=True,
                                  blank=True,
                                  default=settings.MYURLS_DEFAULT_UTM_SOURCE)
    utm_medium = models.CharField(_('Analytics medium'), max_length=80,
        null=True, blank=True, default=settings.MYURLS_DEFAULT_UTM_MEDIUM,
        help_text=_('Media for this campaign (cpc, email, social)'))
    utm_term = models.CharField(_('Analytics term'), max_length=120, null=True,
        blank=True, help_text=_('Keyword for this URL'))
    utm_content = models.CharField(_('Analytics Content'), max_length=80,
        null=True, blank=True, default = settings.MYURLS_DEFAULT_UTM_CONTENT,
        help_text=_('Use to differentiate links that point to the same URL'))
    utm_campaign = models.CharField(_('Analytics Content'), max_length=80,
        null=True, blank=True,
        help_text=_('Use to differentiate links that point to the same URL'),
        default = settings.MYURLS_DEFAULT_UTM_CAMPAIGN)
    append_text = models.CharField(_('Append to URL'), max_length=80, null=True,
        blank=True,
        help_text=_('Additional text to append to url after &'),
        default = settings.MYURLS_DEFAULT_APPEND)
    # add QC fields and a manage.py command to check URLs 

    def save(self, *args, **kwargs):
        """Custom save method that saves short URL to database on save()"""
        # If there is no PK, save and let the DB create one.
        if self.pk is None:
            super(MyUrl, self).save(*args, **kwargs) 
        # create a short url if one isn't there
        if self.short_path == None:
            # create the short path
            path = BaseX(number=self.pk) # Here be the magic
            self.short_path = path.encoded
            # populate the full short URL for later use
            self.short_url = u'%s%s/%s' % (settings.MYURLS_DEFAULT_SCHEME, 
                                           self.site.domain, path)
        # Populate the redirect URL
        self._create_redirect_url()
        # finally, save the model, this time with the short URL.        
        super(MyUrl, self).save(*args, **kwargs)
            
    def _create_redirect_url(self):
        """Checks settigns for MYURLS_USE_UTM and creates a full redirect URL"""
        if settings.MYURLS_USE_UTM == True:
            # If URL has a ? in it start appending GETvars with &
            if self.to_url.find('?') is not None:
                self.redirect_url = u'%s&utm_campaign=%s' % (self.to_url,
                                                             self.utm_campaign)
            else:
                self.redirect_url = u'%s?utm_campaign=%s' % (self.to_url,
                                                             self.utm_campaign)
            if self.utm_term is not None:
                self.redirect_url = u'%s&utm_term=%s' % (self.redirect_url, 
                                                          self.utm_term)
            if self.utm_content is not None:
                self.redirect_url = u'%s&utm_content=%s' % (self.redirect_url, 
                                                             self.utm_content)
            if self.utm_medium is not None:
                self.redirect_url = u'%s&utm_medium=%s' % (self.redirect_url,
                                                            self.utm_medium)
            if self.utm_source is not None:
                self.redirect_url = u'%s&utm_source=%s' % (self.redirect_url,
                                                            self.utm_source)
            # Tack on append text with &
            if self.append_text is not None:
                self.redirect_url = u'%s&%s' % (self.redirect_url, 
                                                self.append_text)        
        else:
            self.redirect_url = self.to_url
            # tack on append text with ? 
            if self.append_text is not None:
                self.redirect_url = u'%s?%s' % (self.redirect_url, 
                                                self.append_text)
                
    def __unicode__(self):
        return u'%s -> %s' % (self.short_url, self.to_url)

    
class Click(models.Model):
    """Model for storing click history."""
    myurl = models.ForeignKey(MyUrl, related_name="clicks")
    user = models.ForeignKey(User, related_name="clicks", null=True, blank=True)
    site = models.ForeignKey(Site, null=True, blank=True)    
    # We can have anonymous users, so there may be no relationship here
    user = models.ForeignKey(User, null=True, related_name="short_url_history")
    to_url = models.URLField(_('Destination  URL'), max_length=200,
        help_text=_('Destination at the time the link was clicked'))
    to_domain = models.CharField(_('Destination Domain'), 
        max_length=200,
        help_text=_('Destination Domain at the time the link was clicked'))
    redirect_url = models.URLField(_('Redirect URL'), max_length=200,
                                   null=True, blank=True)
    created = models.DateTimeField(_('Date & Time'), auto_now_add=True)
    # Optional Referrer Info (it is impossible to know the unknowable)
    user_agent = models.CharField(_('Visitor User Agent'), max_length=300, 
                                  null=True, blank=True)
    user_ip = models.IPAddressField(_('Visitor IP Address'), 
                                    null=True, blank=True)
    user_language = models.CharField(_('Visitor Languages'), max_length=40, 
                                     null=True, blank=True)
    referrer_url = models.URLField(_('Referring URL'), max_length=200,
                                   null=True, blank=True)
    user_domain = models.CharField(_('Referring Domain'), max_length=200,
                                       null=True, blank=True)
    
    def __unicode__(self):
        return self.myurl.short_url

    class Meta:
        """Meta settings for Click object"""
        ordering = ['-created']
        verbose_name = _('Short URL History')
