from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['original_doc', 'translated_doc']
        labels = {
            'original_doc': 'Original document in docx format',
            'translated_doc': 'Translated document in docx format',
        }