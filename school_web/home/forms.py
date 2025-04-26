from django import forms
from .models import KotakSaran

class KotakSaranForm(forms.ModelForm):
    class Meta:
        model = KotakSaran
        fields = ['nama', 'email', 'telepon', 'pesan']
