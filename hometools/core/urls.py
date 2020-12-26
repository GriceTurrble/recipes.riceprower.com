"""hometools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.generic import TemplateView

# (Skip Black formatting in this section)
urlpatterns = [
    # Admin at a non-"admin/" endpoint.
    # Attackers try to hit the common endpoints for the admin, so renaming it something
    # other than the obvious "admin/" is recommended.
    path("nyx/", admin.site.urls),
    # Django account endpoints.
    path("accounts/", include("django.contrib.auth.urls")),
    # TinyMCE's URLs.
    path("tinymce/", include("tinymce.urls")),
    # Stuff for Django REST Framework
    path("api-auth/", include("rest_framework.urls")),
    # Flat pages
    path("pages/", include("django.contrib.flatpages.urls")),
    # Internal apps
    path("invoices/", include("invoices.urls")),
    path("recipes/", include("recipes.urls")),
    # Home page
    path("", TemplateView.as_view(template_name="homepage.html"), name="homepage"),
]

if settings.DEBUG:
    # Serve media files in development server.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
