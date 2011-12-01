from django.contrib import admin
from myurls.models import MyUrl, Click


class MyUrlOption(admin.ModelAdmin):
    """Default shorty admin defs"""
    list_display = ('id', 'created', 'short_url', 'from_url', 'to_url')

admin.site.register(MyUrl, MyUrlOption)
