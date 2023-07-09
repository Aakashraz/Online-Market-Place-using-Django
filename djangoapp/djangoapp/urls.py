"""
URL configuration for djangoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
#  above import of modules:- /settings and static/ - for image to work in index.html
#  since django does not support image file for production i.e. only for development(debug mode)

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),     #required for tailwind css installation

    path('', include('core.urls')),             #this will link to urls.py in core app, then after looping through that urlpatterns in core app,it return back to next line here only
    path('items/', include('item.urls')),       #this will link to urls.py in item app, when call with the url(address)'items/'
    path('dashboard/', include('dashboard.urls')),   #this will link to urls.py in dashboard app
    path('inbox/', include('conversation.urls')),
]

if settings.DEBUG:
    urlpatterns+= static( settings.MEDIA_URL, document_root= settings.MEDIA_ROOT )
