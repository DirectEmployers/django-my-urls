========
Settings
========

The folowing settings are available and can be set in your settings.py:

.. _available-settings:

Available settings
==================
*MYURLS_CHARACTER_SET = "ABCabc123"*
The character set used to encode URLs with. The default is all english language lowercase letters, uppercase letters and numerals. 

*MYURLS_DEFAULT_REDIRECT = '301'*
Default redirect to use for short URLS. 301, 302 and 303 are all valid choices. This default can be overridden when a short url is created and chan be changed by editing the Shorty.redirect_type attribute.

*MYURLS_ALLOW_ALL_SITES*
If you are using the django.contrib.sites framework, MyURLs can allow short urls to work on just the site linked with the myrl or all of your sites.

- *True*: Short URLS will work on all sites.
- *False*: Short URLS will only work on the site linked to the short URL.
 
*MYURLS_USE_UTM (Google Analytics Integraton)*
Activates appending UTM (Urchin Tracking Metrics) codes to urls. This allows Google Analytics to better categorize traffic that is referred via MyURLS. When set to True, the following settings should be configured:
 
 - MYURLS_DEFAULT_UTM_CAMPAIGN
 - MYURLS_DEFAULT_UTM_MEDIUM
 - MYURLS_DEFAULT_UTM_SOURCE
 - MYURLS_DEFAULT_UTM_CONTENT

.._deprecated_settings:

Deprecated Settings
===================

None yet
