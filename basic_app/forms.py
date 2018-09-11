from django import forms
from .models import file


class DocumentForm(forms.ModelForm):
    class Meta:
        model = file
        fields = ('doc1', 'title')
