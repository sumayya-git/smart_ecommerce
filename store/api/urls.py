from django.urls import path
from .views import *
from .views import user_profile, update_profile
from .views import VerifyPaymentAPIView
from .views import register
from .views import get_categories
from .views import( verify_invoice,pay_order,OrderInvoiceAPI,OrderDetailAPI,          
AdminOrderDetailAPIView,revenue_report,revenue_csv,AdminDashboardStateAPIView,
AdminTopProductsAPIView,MonthlyReportAPIView)
from .views import (DecreaseCartItemAPI,CartDetailAPIView, AddToCartAPIView, RemoveFromCartAPIView,UpdateOrderStatusAPIView,
                    AdminUpdateOrderAPIView,AdminRefundAPIView)
from .views import( LoginView,ProductListAPIView,ProductDetailAPIView, MyOrdersAPIView, CancelOrderAPIView,
                    OrderCreateAPIView,AdminOrdersAPIView,CreatePaymentOrderAPIView,RequestReturnAPIView, csrf)


from .views import celery_test



urlpatterns = [

    path("celery-test/", celery_test),
    
    path("cart/add/<int:product_id>/", AddToCartAPIView.as_view(), name="add-to-cart"),

   


    path("cart/remove/<int:item_id>/", RemoveFromCartAPIView.as_view()),
    path("products/",ProductListAPIView.as_view(), name="product-list"),
    path("products/<int:pk>/",ProductDetailAPIView.as_view(), name="product-detail"),
    path("my-orders/",MyOrdersAPIView.as_view()),
    path("order/cancel/<int:order_id>/", CancelOrderAPIView.as_view()),
    path("order/create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("order/update-status/<int:order_id>/",UpdateOrderStatusAPIView.as_view()),
    path("admin/orders/",AdminOrdersAPIView.as_view()),
    path("order/<int:pk>/",OrderDetailAPI.as_view(), name="order-detail"),
    path("admin/order/update/<int:order_id>/",AdminUpdateOrderAPIView.as_view()),
    path("admin/order/<int:order_id>/",AdminOrderDetailAPIView.as_view()),
    path("admin/dashboard/",AdminDashboardStateAPIView.as_view()),
    path("admin/top-products/",AdminTopProductsAPIView.as_view()),
    path("admin/monthly-report/",MonthlyReportAPIView.as_view()),
    path("admin/refund/<int:order_id>/",AdminRefundAPIView.as_view()),
    path("order/pay/<int:order_id>/",pay_order),
    path("admin/revenue/", revenue_report),
    path("admin/revenue-csv/", revenue_csv),
    path('payment/create-order/', CreatePaymentOrderAPIView.as_view(), name='create-payment-order'),
    path('verify-payment/', VerifyPaymentAPIView.as_view(), name='verify-payment'),
    path("order/<int:pk>/invoice/", OrderInvoiceAPI.as_view(), name="order-invoice"),
    path("verify-invoice/<int:order_id>/", verify_invoice),
    path("register/",register),
    path('profile/', user_profile),
    path("update-profile/",update_profile),
     path("order/<int:order_id>/return/", RequestReturnAPIView.as_view()),
    path('categories/',get_categories),
    # path("order/pay/", MarkOrderPaidAPIView.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view()),
    path('cart/decrease/<int:product_id>/',DecreaseCartItemAPI.as_view()),
    path('cart/',CartDetailAPIView.as_view()),
    path("csrf/", csrf),
    path("order/<int:order_id>/refund-details/",RefundDetailsAPIView.as_view()),

    
]