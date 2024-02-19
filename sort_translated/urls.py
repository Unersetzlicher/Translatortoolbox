# sort_translated/urls.py

from django.urls import path
from .views import sort_translated_view, sorted_output_view  # Import your view function

urlpatterns = [
    path('sort/', sort_translated_view, name='sort_translated'),  # Existing URL pattern
    path('sorted_output/', sorted_output_view, name='sorted_output'),  # New URL pattern
]
