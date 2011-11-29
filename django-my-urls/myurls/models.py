from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from basex import BaseX, BaseXError
from django.conf import settings

class MyUrl(models.Model):
    """Short url model. Domains are pulled from the django.contrib.sites.

    Short URLs are this models PK encoded in baseX using
    settings.SHORTY_CHARACTER_SET.

    Attributes:

    from_site -- Site responsible for creating the shorty
    from_url -- URL responsible for creating the shorty
    to_url -- the destination URL
    shorty -- the short URL
    redirect_type -- the type of redirect to return
    notes -- user notes
    created -- creation timestamp
    utm_source -- Google analytics source
    utm_medium -- Google analytics medium
    utm_term -- Google analytics search keyword
    utm_content -- Google analytics content
    utm_campaign -- Google analytics campaign
    """

    CHOICES = (
        (_('301 - permanent'), '301'),
        (_('302 - unspecified'), '302'),
        (_('303 - see other'), '303'),
        (_('307 - temporary'), '307'),
        )
    created = models.DateTimeField(_('Created on'), auto_now_add=True)
    site = models.ForeignKey(Site, related_name="short_urls",
                             default=settings.SITE_ID)
    from_url = models.URLField(_('Source URL'), max_length=200,
        help_text=_('URL where shorty was created'), null=True, blank=True)
    to_url = models.URLField(_('Destination URL'),
        help_text=_('Full URL including scheme (http://, ftp://, etc...'))
    redirect_url=models.URLField(_('URL to send user to'), max_length=300, 
                                 blank=True, null=True)
    short_path = models.CharField(_('Encoded IDdbd'), max_length=10,
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
                                  default='myjobs')
    utm_medium = models.CharField(_('Analytics medium'), max_length=80,
        null=True, blank=True, default=settings.MYURLS_DEFAULT_UTM_MEDIUM,
        help_text=_('Media for this campaign (cpc, email, social)'))
    utm_term = models.CharField(_('Analytics term'), max_length=120, null=True,
        blank=True, help_text=_('Keyword for this URL'))
    utm_content = models.CharField(_('Analytics Content'), max_length=80,
        null=True, blank=True, default = settings.MYURLS_DEFAULT_CONTENT,
        help_text=_('Use to differentiate links that point to the same URL'))
    utm_campaign = models.CharField(_('Analytics Content'), max_length=80,
        null=True, blank=True,
        help_text=_('Use to differentiate links that point to the same URL'),
        default = settings.MYRULS_DEFAULT_UTM_CAMPAIGN)
    # TODO add QC fields and a manage.py command to check URLs 

    def save(self):
        """Custom save method that saves short URL to database on save()"""
        # standard save, populate and save pattern
        # this lets the db create the primary key, and then allows us
        # to populate attribues.
        super(MyUrl, self).save() 
        if self.short_path == None:
            # create the short path
            path = BaseX(number=self.pk)
            self.short_path = path.encoded
            # populate the full destination URL
            self.short_url = u'%s%s/%s' % (settings.MYURLS_DEFAULT_SCHEME, 
                                           self.site.domain, path)            
    def _create_redirect_url(self):
        """Creates a full redirect URL"""
        if settings.MYURLS_USE_UTM == True:
            self.redirect_url = 'u%s?utm_campaign=%s' % (self.to_url,
                self.utm_campaign)
            if self.utm_term is not None:
                self.redirect_url = u'%s&utm_term=%s' % s(self.redirect_url, 
                                                          self.utm_term)
            if self.utm_content is not None:
                self.redirect_url = u'%s&utm_content=%s' % s(self.redirect_url, 
                                                             self.utm_content)
        else:
            self.redirect_url = self.to_url
            
        # finally, save the model, this time with the short URL.        
        super(MyUrl, self).save() 

    def __unicode__(self):
        return u'%s -> %s' % (self.short_url, self.to_url)

    
class Click(models.Model):
    """Stores click history"""
    site = models.ForeignKey(Site, null=True, blank=True)
    # We can have anonymous users, so there may be no relationship here
    user = models.ForeignKey(User, null=True, related_name="short_url_history")
    visitor = models.ForeignKey(User, blank=True, null=True)
    destination_url = models.URLField(_('Destination  URL'), max_length=200,
        help_text=_('Destination at the time the link was clicked'))
    destination_domain = models.CharField(_('Destination Domain'), max_length=200,
        help_text=_('Destination Domain at the time the link was clicked'))
    created = models.DateTimeField(_('Date & Time'), auto_now_add=True)
    # Optional Referrer Info (it is impossible to know the unknowable)
    referrer_url = models.URLField(_('Referring URL'), max_length=200,
                                   null=True, blank=True)
    referrer_domain = models.CharField(_('Referring Domain'), max_length=200,
                                       null=True, blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Short URL History')
