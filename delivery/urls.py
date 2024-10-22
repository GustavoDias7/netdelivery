"""
URL configuration for delivery project.

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
from django.urls import path
from apps.core import views
from apps.core.admin import autocomplete_view

# change the autocomplete text content
admin.AdminSite.autocomplete_view = autocomplete_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.homepage, name="homepage"),
    path("cadastro", views.signup, name="signup"),
    path("login", views.signin, name="signin"),
    path("logout", views.logout_view, name="logout"),
    path("pedido", views.order, name="order"),
    path("conta", views.account, name="account"),
    path("conta/perfil", views.profile, name="profile"),
    path("conta/perfil/editar", views.edit, name="edit"),
    path("conta/pedidos", views.orders, name="orders"),
    path("conta/endereco", views.address, name="address"),
    path("conta/endereco/editar", views.address_edit, name="address_edit"),
]
