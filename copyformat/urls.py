# copyformat/urls.py
from django.urls import path
from .views import upload_file, download_file, success_view, home

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_file, name='upload_file'),
    path('download/', download_file, name='download_file'),
    path('success/', success_view, name='success_view'),
]
