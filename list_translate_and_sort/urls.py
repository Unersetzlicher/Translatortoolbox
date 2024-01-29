# list_translate_and_sort/urls.py
from django.urls import path
from .views import process_string

urlpatterns = [
    path('', process_string, name='process_string'),
]

