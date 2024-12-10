from django.contrib import admin
from django.urls import path
from apps.core import views as core_views
from apps.product import views as product_views
from apps.order import views as order_views
from apps.address import views as address_views
from apps.user import views as user_views
from apps.core.admin import autocomplete_view
from django.conf import settings
from django.conf.urls.static import static

# change the autocomplete text content
admin.AdminSite.autocomplete_view = autocomplete_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("<slug:username>/", core_views.homepage, name="homepage"),
    path("<slug:username>/produto/", product_views.product, name="product"),
    path("<slug:username>/combo/", product_views.combo, name="combo"),
    path("<slug:username>/cadastro/", user_views.signup, name="signup"),
    path("<slug:username>/login/", user_views.signin, name="signin"),
    path("<slug:username>/logout/", user_views.logout_view, name="logout"),
    path("<slug:username>/pedido/", order_views.order, name="order"),
    path("<slug:username>/conta/", user_views.account, name="account"),
    path("<slug:username>/conta/perfil", user_views.profile, name="profile"),
    path("<slug:username>/conta/perfil/editar", user_views.edit, name="edit"),
    path("<slug:username>/conta/pedidos", order_views.orders, name="orders"),
    path("<slug:username>/conta/endereco/", address_views.address, name="address"),
    path("<slug:username>/conta/endereco/editar/", address_views.address_edit, name="address_edit"),
    path("<slug:username>/sucesso", order_views.success, name="success"),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)