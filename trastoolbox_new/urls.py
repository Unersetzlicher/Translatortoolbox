"""
URL configuration for trastoolbox_new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from copyformat.views import home

urlpatterns = [
    path('', home, name='home'),
    path('list_translate_and_sort/', include('list_translate_and_sort.urls')),
    path('copyformat/', include('copyformat.urls')),
    path('sort_translated/', include('sort_translated.urls')),
    # ... other paths ...
]