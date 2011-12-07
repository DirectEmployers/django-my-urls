# admin.py

from django.contrib import admin
from myurls.models import MyUrl, Click


class MyUrlOption(admin.ModelAdmin):
    """Default shorty admin defs"""
    list_display = ('id', 'created', 'short_url', 'from_url', 'to_url')

class ClickOption(admin.ModelAdmin):
    """Clickstream history admin"""
    list_display = ('id', 'created', 'myurl', 'user')

admin.site.register(MyUrl, MyUrlOption)
admin.site.register(Click, ClickOption)
