"""
URL configuration for staffix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('aboutus/', views.aboutus ,name='aboutus'),
    path('contact/', views.contact , name='contact'),
    path('login/', views.login , name='login'),
    path('logout/', views.logout , name='logout'),
    path('view-more-jobs/', views.viewmore_job , name='viewmore_job'),
    path('job/<slug:job_slug>/', views.job_detail , name='job_detail'),
    path('apply/<slug:job_slug>/', views.apply_job , name='apply_job'),
    path('', include("admin_app.urls")),
    path('', include("user_app.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
