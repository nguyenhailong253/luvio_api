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
    path("login/", views.LoginView.as_view(), name="login"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    # Ref: https://stackoverflow.com/a/9744268/8749888 - end slash
    # Ref: https://stackoverflow.com/a/51922669/8749888 - name attribute
    path("accounts/password/", views.change_password, name="change-password"),
    path("accounts/", views.UserAccountView.as_view(), name="accounts"),
    path(
        "profiles/<int:id>/",
        views.UserProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path("profiles/", views.UserProfileListView.as_view(), name="profiles"),
    path(
        "profiles/tenant-profiles/<int:profile_id>/addresses/",
        views.TenantProfilesAddressesView.as_view(),
        name="tenant-profiles-addresses",
    ),
    path(
        "profiles/agent-profiles/<int:profile_id>/addresses/",
        views.AgentProfilesAddressesView.as_view(),
        name="agent-profiles-addresses",
    ),
    path("profile-types/", views.ProfileTypeView.as_view(), name="profile-types"),
    path(
        "addresses/suggestions/",
        views.get_address_suggestions,
        name="address-suggestions",
    ),
]
