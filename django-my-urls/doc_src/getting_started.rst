
Getting Started
===============
*Fast Way:* Go to example directory and start hacking.
*Methodical Way:* Add myurls to your installed apps in settings.py.

Two methods are provided for implementing short URL redirection:

- a 404 FallbackMiddleWare and a view. 
- a django view

*When to use the FallBackMiddleWare:*

- When every URL except those in URLs.py are short URLs
- eg. mysite.com/si11S

* When to use the view based redirector:*
- When you need all URLs following a URL pattern to be redirected.
- eg. mysite.com/click/si11S