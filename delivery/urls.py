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
from apps.core import views as core_views
from apps.product import views as product_views
from apps.core.admin import autocomplete_view

# change the autocomplete text content
admin.AdminSite.autocomplete_view = autocomplete_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", core_views.homepage, name="homepage"),
    path("produto", product_views.product, name="product"),
    path("combo", product_views.combo, name="combo"),
    path("cadastro", core_views.signup, name="signup"),
    path("login", core_views.signin, name="signin"),
    path("logout", core_views.logout_view, name="logout"),
    path("pedido", core_views.order, name="order"),
    path("conta", core_views.account, name="account"),
    path("conta/perfil", core_views.profile, name="profile"),
    path("conta/perfil/editar", core_views.edit, name="edit"),
    path("conta/pedidos", core_views.orders, name="orders"),
    path("conta/endereco", core_views.address, name="address"),
    path("conta/endereco/editar", core_views.address_edit, name="address_edit"),
]
