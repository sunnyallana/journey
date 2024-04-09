"""
URL configuration for journey project.

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
from django.urls import path, include

from django.contrib.sitemaps.views import sitemap
from blogApplication.sitemaps import PostSitemap

# The sitemaps dictionary is used to define the sitemaps for your site. The keys are the names of the sitemaps, and the values are the sitemap classes.
sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # The namespace attribute is used to specify the application namespace. This is useful when you want to reference a URL pattern from another application.
    # Access namespace in the template using the following syntax: {% url 'blogApplication:post_list' %}
    path('blog/', include('blogApplication.urls',namespace='blogApplication')), 
    # The sitemap() function is a Django view that generates the sitemap XML file for your site. The sitemap view takes a dictionary of sitemaps as an argument.
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
