from django.contrib import admin
from django.urls import path,include
from .import views
from .views import login_view, add_to_cart, view_cart, remove_from_cart



urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', view_cart, name='cart'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/remove/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/',views.order_success,name='order_success'),
    path('order-status/',views.order_status,name='order_status'),
    path('track-order/<int:order_id>/',views.track_order, name='track_order'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('increase/<int:id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:id>/',views.decrease_qty, name='decrease_qty'),
    path('place-order/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path("order/<int:order_id>/invoice/", views.invoice_pdf, name="invoice_pdf"),
    path('admin/', admin.site.urls),
    path('api/', include('store.api.urls')),
    path("cancel-order/<int:order_id>/",views.cancel_order, name="cancel_order"),
    path("order-item/reduce/<int:item_id>/", views.reduce_order_item, name="reduce_order_item"),
    path("order-item/increase/<int:item_id>/", views.increase_order_item, name="increase_order_item"),
    # path("send-invoice/<int:order_id>/", views.send_invoice_email, name="send_invoice_email"),
]