Middleware
==========
Django-my-urls can use Django's fallback middleware to redirect short URLS. The
primary advantage of this is that it allows MyUrls to work with other redirect
apps and handle all URLS that are not part of your site's URLs as defined in 
urls.py.

.. automodule:: myurls.middleware
   :members: