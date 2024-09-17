"""
URL configuration for dev_search project.

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
from django.conf import settings
from django.conf.urls.static import static

#so below if we set the path empty the first page to be opened will be the respective page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/',include('projects.urls')),
    path('',include('users.urls')),
    path('api/',include('api.urls')),
]

#to make django know from where to load the images on the web page
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)