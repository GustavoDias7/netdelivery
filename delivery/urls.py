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
from apps.order import views as order_views
from apps.address import views as address_views
from apps.user import views as user_views
from apps.core.admin import autocomplete_view

# change the autocomplete text content
admin.AdminSite.autocomplete_view = autocomplete_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", core_views.homepage, name="homepage"),
    path("produto", product_views.product, name="product"),
    path("combo", product_views.combo, name="combo"),
    # path("cadastro", user_views.signup, name="signup"),
    # path("login", user_views.signin, name="signin"),
    path("logout", user_views.logout_view, name="logout"),
    # path("pedido", order_views.order, name="order"),
    # path("conta", user_views.account, name="account"),
    # path("conta/perfil", user_views.profile, name="profile"),
    # path("conta/perfil/editar", user_views.edit, name="edit"),
    # path("conta/pedidos", order_views.orders, name="orders"),
    # path("conta/endereco", address_views.address, name="address"),
    # path("conta/endereco/editar", address_views.address_edit, name="address_edit"),
]
