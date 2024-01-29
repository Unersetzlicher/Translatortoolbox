# string_processor/forms.py
from django import forms


class StringForm(forms.Form):
    input_string = forms.CharField(label='Enter your list', max_length=5000)
