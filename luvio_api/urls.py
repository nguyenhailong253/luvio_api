"""luvio_api URL Configuration

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
from django.urls import path

from luvio_api import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # AUTHENTICATION
    path("login/", views.LoginView.as_view(), name="login"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    # Ref: https://stackoverflow.com/a/9744268/8749888 - end slash
    # Ref: https://stackoverflow.com/a/51922669/8749888 - name attribute
    # ACCOUNTS
    path("accounts/password/", views.change_password, name="change-password"),
    path("accounts/", views.UserAccountView.as_view(), name="accounts"),
    # PROFILES
    path(
        "profiles/<int:profile_id>/",
        views.UserProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path("profiles/", views.UserProfileListView.as_view(), name="profiles"),
    path(
        "profiles/public/<str:profile_uri>/",
        views.get_public_profile,
        name="public-profile",
    ),
    path(
        "profiles/<int:profile_id>/addresses/",
        views.ProfilesAddressesListView.as_view(),
        name="profiles-addresses",
    ),
    path(
        "profiles/<int:profile_id>/addresses/<int:profile_address_id>/",
        views.ProfilesAddressesDetailView.as_view(),
        name="profiles-addresses-detail",
    ),
    # PROFILE TYPES
    path("profile-types/", views.ProfileTypeView.as_view(), name="profile-types"),
    # ADDRESS SUGGESTIONS
    path(
        "addresses/suggestions/",
        views.get_address_suggestions,
        name="address-suggestions",
    ),
]
