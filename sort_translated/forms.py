from django import forms

class SortForm(forms.Form):
    input_string = forms.CharField(label='Enter your translated list', widget=forms.Textarea)
