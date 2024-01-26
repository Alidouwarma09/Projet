from django import forms
from .models import SiteParameters


class SiteParametersForm(forms.ModelForm):
    class Meta:
        model = SiteParameters
        fields = '__all__'
