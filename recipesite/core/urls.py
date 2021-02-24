"""recipesite URL Configuration

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

# (Skip Black formatting in this section)
urlpatterns = [
    # Admin at a non-"admin/" endpoint.
    # Attackers try to hit the common endpoints for the admin, so renaming it something
    # other than the obvious "admin/" is recommended.
    path("admit-tenant-tiger/", admin.site.urls),
    # Django account endpoints.
    path("accounts/", include("django.contrib.auth.urls")),
    # TinyMCE's URLs.
    path("tinymce/", include("tinymce.urls")),
    # Flat pages (TODO out for now)
    # path("pages/", include("django.contrib.flatpages.urls")),
    # Internal apps
    # path("invoices/", include("invoices.urls")),
    path("", include("recipes.urls")),
    # Home page
    # Django REST Framework
    # TODO not using REST at this time. Do this later, though!
    # path("api-auth/", include("rest_framework.urls")),
    # path("api/v1/", include("core.api_v1.urls")),
    # path("api/auth/", include("djoser.urls.authtoken")),
    # path("api/", RedirectView.as_view(url='/api/v1/')),
]

if settings.DEBUG:
    # Serve media files in development server.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
