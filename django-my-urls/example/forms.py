# forms.py
from django.forms import ModelForm
from myurls.models import MyUrl

class CreateMyUrlForm(ModelForm):
    """Simple form for creating a MyUrl"""
    class Meta:
        model=MyUrl
        exclude=('created', 'from_url', 'site', 'short_url', 'short_path', 'user', 'redirect_url',)
        
        
class EditMyUrlForm(ModelForm):
    """Simple form for editing a MyUrl. Log in to admin before trying"""
    
    class Meta:
        model=MyUrl
    
