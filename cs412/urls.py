"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.urls')),
    # path('hw/', include('hw.urls')),  ## Creates URL hw/, and associates it with other URLS in hw.urls
    # path('quotes/', include('quotes.urls')), ## Creates URL quotes/, and associates it with other URLS in quotes.urls
    # path('restaurant/', include('restaurant.urls')),
    # path('formdata/', include('formdata.urls')),
    # path('blog/', include('blog.urls')), # include the URLs from our blog project's urls.py file
    # path('mini_fb/', include('mini_fb.urls')), # include the URLs from our blog project's urls.py file
    # path('ma/', include('marathon_analytics.urls')), # include the URLs
    # path('va/', include('voter_analytics.urls')), # include the URLs
    path('project/', include('project.urls')), # include the URLs
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

