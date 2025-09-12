from django.urls import path
from .apiviews import InitiatePaymentView, ListOrdersView, DeleteOrderView, VerifyPaymentAPIView
app_name = "orders"
urlpatterns = [
    path('initiate-payment', InitiatePaymentView.as_view(), name='order-create'),
    path('list', ListOrdersView.as_view(), name='order-list'),
    path('verify-payment/<reference>', VerifyPaymentAPIView.as_view(), name='verify-payment'),
    # path('verify-payment', verify_payment, name='verify-payment'),
    # path('update/<uuid:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('delete/<pk>/', DeleteOrderView.as_view(), name='order-delete'),
]
