"""speedolearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

# from grappelli import urls as grappelli_urls
from superadmin import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/training/", include("training.urls"), name="training-api"),
    path("api/admin/", include("superadmin.urls"), name="admin-api"),
    # path("grappelli/", include(grappelli_urls)),  # Grappelli URLS
    path("api/login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.BUILD_URL, document_root=settings.BUILD_URL)
