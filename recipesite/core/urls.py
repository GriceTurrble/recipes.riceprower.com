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
from django.shortcuts import redirect, render

from accounts.views import LoginView

# from accounts.views import RegisterView
from accounts.views import logout_view


def index_view(request):
    """Quick index template view that redirects to recipes
    if the user is already logged in.
    """
    if request.user.is_authenticated:
        return redirect("recipes:recipe-list")
    return render(request, "index.html", {})


# (Skip Black formatting in this section)
urlpatterns = [
    # Admin at a non-"admin/" endpoint.
    # Attackers try to hit the common endpoints for the admin, so renaming it something
    # other than the obvious "admin/" is recommended.
    path("admit-tenant-tiger/", admin.site.urls),
    # Custom account handling views
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    # path("register/", RegisterView.as_view(), name="register"),
    # TinyMCE's URLs.
    path("tinymce/", include("tinymce.urls")),
    # Internal apps
    path("recipes/", include("recipes.urls")),
    # Other views
    path("", index_view, name="index"),
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
